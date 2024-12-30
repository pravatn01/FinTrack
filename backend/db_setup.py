import mysql.connector

conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

if conn.is_connected():
    print('Connected')
    cursor = conn.cursor(dictionary=True)
    cursor.execute('select * from expenses')
    expenses = cursor.fetchall()

    for expense in expenses:
        print(expense)

cursor.close()
conn.close()
