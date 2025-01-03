import mysql.connector
from contextlib import contextmanager
from logger import setup_logger

logger = setup_logger('db_setup')

@contextmanager
def get_db_cursor(commit=False):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    cursor = conn.cursor(dictionary=True)
    yield cursor
    if commit:
        conn.commit()
    cursor.close()
    conn.close()

def fetch_expenses_for_date(expense_date, table_name="expenses"):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute(f'SELECT * FROM {table_name} WHERE expense_date = %s', (expense_date,))
        expenses = cursor.fetchall()
        return expenses

def insert_expense(expense_date, amount, category, notes, table_name="expenses"):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            f'INSERT INTO {table_name} (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)',
            (expense_date, amount, category, notes)
        )

def delete_expenses_for_date(expense_date, table_name="expenses"):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(f'DELETE FROM {table_name} WHERE expense_date = %s', (expense_date,))

def fetch_expense_summary(start_date, end_date, table_name="expenses"):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            f'''
            SELECT category, SUM(amount) AS total
            FROM {table_name}
            WHERE expense_date BETWEEN %s AND %s
            GROUP BY category
            ''',
            (start_date, end_date)
        )
        summary = cursor.fetchall()
        return summary


# if __name__ == '__main__':
#     print(fetch_expenses_for_date('2024-08-06'))
