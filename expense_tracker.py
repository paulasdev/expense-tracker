import tkinter as tk
from tkinter import messagebox
import sqlite3
from matplotlib import pyplot as plt

# Database initialization
conn = sqlite3.connect("expenses.db")
c = conn.cursor()

# Create expenses table if not exists
c.execute(
    """CREATE TABLE IF NOT EXISTS expenses
             (id INTEGER PRIMARY KEY, category TEXT, amount REAL, date TEXT)"""
)
conn.commit()


# Function to add expense to database
def add_expense():
    category = category_entry.get()
    amount = amount_entry.get()
    date = date_entry.get()

    if category and amount and date:
        c.execute(
            "INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
            (category, amount, date),
        )
        conn.commit()
        messagebox.showinfo("Success", "Expense added successfully!")
        clear_entries()
        update_graph()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")
