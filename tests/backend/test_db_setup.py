import pytest
from backend.db_setup import (
    insert_expense,
    fetch_expenses_for_date,
    delete_expenses_for_date,
    fetch_expense_summary,
    get_db_cursor,
)

TABLE_NAME = "test_expenses"  

@pytest.fixture(scope="module")
def setup_test_db():
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            expense_date DATE NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            category VARCHAR(50),
            notes TEXT
        )
        ''')
    yield

    with get_db_cursor(commit=True) as cursor:
        cursor.execute(f'DROP TABLE IF EXISTS {TABLE_NAME}')

@pytest.fixture(scope="function")
def reset_test_db():
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(f'TRUNCATE TABLE {TABLE_NAME}')

def test_insert_expense(setup_test_db, reset_test_db):
    insert_expense("2025-01-01", 100.00, "Food", "Lunch", table_name=TABLE_NAME)
    expenses = fetch_expenses_for_date("2025-01-01", table_name=TABLE_NAME)
    assert len(expenses) == 1
    assert expenses[0]["amount"] == 100.00
    assert expenses[0]["category"] == "Food"
    assert expenses[0]["notes"] == "Lunch"

def test_fetch_expenses_for_date(setup_test_db, reset_test_db):
    insert_expense("2025-01-02", 50.00, "Transport", "Bus fare", table_name=TABLE_NAME)
    expenses = fetch_expenses_for_date("2025-01-02", table_name=TABLE_NAME)
    assert len(expenses) == 1
    assert expenses[0]["amount"] == 50.00
    assert expenses[0]["category"] == "Transport"
    assert expenses[0]["notes"] == "Bus fare"

def test_delete_expenses_for_date(setup_test_db, reset_test_db):
    insert_expense("2025-01-03", 75.00, "Entertainment", "Movie night", table_name=TABLE_NAME)
    delete_expenses_for_date("2025-01-03", table_name=TABLE_NAME)
    expenses = fetch_expenses_for_date("2025-01-03", table_name=TABLE_NAME)
    assert len(expenses) == 0

def test_fetch_expense_summary(setup_test_db, reset_test_db):
    insert_expense("2025-01-04", 40.00, "Utilities", "Electricity bill", table_name=TABLE_NAME)
    insert_expense("2025-01-05", 60.00, "Utilities", "Water bill", table_name=TABLE_NAME)
    summary = fetch_expense_summary("2025-01-01", "2025-01-06", table_name=TABLE_NAME)
    assert len(summary) == 1
    assert summary[0]["category"] == "Utilities"
    assert summary[0]["total"] == 100.00
