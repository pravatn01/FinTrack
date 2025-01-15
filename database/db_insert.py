# This is a script to insert some data onto the expenses table of database.
# Either import the 'expense_db_backup.sql' onto MySQL database or run this script.


import random
import mysql.connector
from datetime import datetime, timedelta

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "expense_manager"
}

categories = [
    "Entertainment",
    "Food",
    "Rent",
    "Shopping",
    "Others"
]

notes = {
    "Entertainment": ["Movie tickets", "Concert tickets", "Theater tickets", "Video rental", "Streaming subscription"],
    "Food": ["Groceries", "Lunch", "Dinner at a restaurant", "Snacks", "Coffee", "Fast food", "Takeout"],
    "Rent": ["Monthly rent payment", "Shared rent payment"],
    "Shopping": ["Clothes", "Electronics", "Home supplies", "Books", "Shoes", "Gadgets", "Cosmetics"],
    "Others": ["Gasoline", "Public transport", "Parking fee", "Miscellaneous", "Unplanned purchase"]
}

def generate_expense_data():
    expense_data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    current_date = start_date
    while current_date <= end_date:
        num_entries = random.randint(1, 10)
        for _ in range(num_entries):
            category = random.choice(categories)
            note = random.choice(notes[category])
            amount = random.randint(10, 500)
            expense_entry = {
                "expense_date": current_date.strftime("%Y-%m-%d"),
                "amount": amount,
                "category": category,
                "notes": note
            }
            expense_data.append(expense_entry)
        current_date += timedelta(days=1)
    return expense_data

def create_database_and_table():
    conn = mysql.connector.connect(host="localhost", user="root", password="root")
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS expense_manager")
    conn.database = "expense_manager"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            expense_date DATE NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            category VARCHAR(50),
            notes TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


def insert_expense_data(expense_data):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO expenses (expense_date, amount, category, notes)
    VALUES (%s, %s, %s, %s)
    """
    for entry in expense_data:
        cursor.execute(insert_query, (entry["expense_date"], entry["amount"], entry["category"], entry["notes"]))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_database_and_table()
    expense_data = generate_expense_data()
    insert_expense_data(expense_data)
    print(f"Inserted {len(expense_data)} records into the database.")
