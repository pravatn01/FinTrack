import mysql.connector
from contextlib import contextmanager

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

def fetch_expenses_for_date(expense_date):
    with get_db_cursor() as cursor:
        cursor.execute('select * from expenses where expense_date = %s', (expense_date,))
        expenses = cursor.fetchall()
        return expenses

def insert_expense(expense_date,amount,category,notes):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute('insert into expenses (expense_date,amount,category,notes) values(%s,%s,%s,%s)',(expense_date,amount,category,notes))

def delete_expenses_for_date(expense_date):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute('delete from expenses where expense_date = %s', (expense_date,))

def fetch_expense_summary(start_date, end_date):
    with get_db_cursor() as cursor:
        cursor.execute('''SELECT category, sum(amount) as total
                          from expenses
                          WHERE expense_date BETWEEN %s AND %s
                          GROUP BY category''',(start_date, end_date))
        summary = cursor.fetchall()
        return summary

if __name__ == '__main__':
    # expenses = fetch_expenses_for_date('2024-08-05')
    # for expense in expenses:
    #     print(expense)

    # insert_expense('2024-09-30', 20, 'hello', 'hello')

    # delete_expenses_for_date('2024-09-30')

    summary = fetch_expense_summary('2024-08-01', '2024-08-05')
    for data in summary:
        print(data)