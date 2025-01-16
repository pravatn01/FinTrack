from fastapi import FastAPI, HTTPException
from datetime import date
from typing import List
from pydantic import BaseModel
import backend.db_setup as db_setup

app = FastAPI()

class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses = db_setup.fetch_expenses_for_date(expense_date)
    if not expenses:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses.")
    return expenses

@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses: List[Expense]):
    db_setup.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_setup.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
    return {"message": "Expenses updated successfully"}

@app.post('/category_summary/')
def get_category_summary(date_range: DateRange):
    data = db_setup.fetch_category_expense_summary(date_range.start_date, date_range.end_date)
    if not data:
        raise HTTPException(status_code=500, detail="Failed to retrieve category expense summary.")
    total = sum(row['total'] for row in data)
    breakdown = {
        row['category']: {
            'total': row['total'],
            'percentage': (row['total'] / total) * 100 if total else 0
        }
        for row in data
    }
    return breakdown

@app.get("/monthly_summary/")
def get_monthly_summary():
    monthly_summary = db_setup.fetch_monthly_expense_summary()
    if not monthly_summary:
        raise HTTPException(status_code=500, detail="Failed to retrieve monthly expense summary.")
    return monthly_summary
