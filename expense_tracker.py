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


# Function to clear entry fields
def clear_entries():
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)


# Function to update expense graph
def update_graph():
    c.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = c.fetchall()
    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(6, 4))
    plt.bar(categories, amounts)
    plt.xlabel("Categories")
    plt.ylabel("Amount")
    plt.title("Expense Distribution")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
