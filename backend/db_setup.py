import mysql.connector
from contextlib import contextmanager
from backend.logger import setup_logger

logger = setup_logger('db_setup')

@contextmanager
def get_db_cursor(commit=False):
    conn = mysql.connector.connect(
        host="localhost", user="root", password="root", database="expense_manager"
    )
    cursor = conn.cursor(dictionary=True)
    try:
        yield cursor
        if commit:
            conn.commit()
    finally:
        cursor.close()
        conn.close()

def fetch_expenses_for_date(expense_date, table_name="expenses"):
    logger.info(f"Fetching expenses for {expense_date} from {table_name}")
    with get_db_cursor() as cursor:
        cursor.execute(f'SELECT * FROM {table_name} WHERE expense_date = %s', (expense_date,))
        return cursor.fetchall()

def insert_expense(expense_date, amount, category, notes, table_name="expenses"):
    logger.info(f"Inserting expense on {expense_date} for {amount} in {category}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            f'INSERT INTO {table_name} (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)',
            (expense_date, amount, category, notes)
        )

def delete_expenses_for_date(expense_date, table_name="expenses"):
    logger.info(f"Deleting expenses for {expense_date} from {table_name}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(f'DELETE FROM {table_name} WHERE expense_date = %s', (expense_date,))

ALLOWED_TABLES = {"expenses", "test_expenses"}

def fetch_category_expense_summary(start_date, end_date, table_name="expenses"):
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"Invalid table name: {table_name}")
    logger.info(f"Fetching category summary for {start_date} to {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            f'''SELECT category, SUM(amount) AS total
               FROM {table_name}
               WHERE expense_date BETWEEN %s AND %s
               GROUP BY category''',
            (start_date, end_date)
        )
        return cursor.fetchall()

def fetch_monthly_expense_summary():
    logger.info("Fetching monthly expense summary")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT MONTH(expense_date) AS expense_month,
                      MONTHNAME(expense_date) AS month_name,
                      SUM(amount) AS total
               FROM expenses
               GROUP BY expense_month, month_name
               ORDER BY expense_month'''
        )
        return cursor.fetchall()
