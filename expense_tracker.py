import tkinter as tk
from tkinter import messagebox
import sqlite3
from matplotlib import pyplot as plt

# Database initialization
conn = sqlite3.connect("expenses.db")
c = conn.cursor()

# Create expenses table if not exists
try:
    c.execute(
        """CREATE TABLE IF NOT EXISTS expenses
             (id INTEGER PRIMARY KEY, category TEXT, amount REAL, date TEXT)"""
    )
    conn.commit()
except sqlite3.Error as e:
    print("Error creating expenses table:", e)


# Function to add expense to database
def add_expense():
    category = category_entry.get()
    amount = amount_entry.get()
    date = date_entry.get()

    # Convert date format from input format to DD/MM/YYYY
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")
    except ValueError:
        messagebox.showerror(
            "Error", "Invalid date format. Please enter date in YYYY-MM-DD format."
        )
        return

    if category and amount and date:
        try:
            c.execute(
                "INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
                (category, amount, date),
            )
            conn.commit()
            messagebox.showinfo("Success", "Expense added successfully!")
            clear_entries()
            update_graph()
        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error",
                "An error occurred while adding the expense: " + str(e),
            )
    else:
        messagebox.showerror("Error", "Please fill in all fields.")


# Function to clear entry fields
def clear_entries():
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)


# Function to update expense graph
def update_graph():
    try:
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
    except sqlite3.Error as e:
        messagebox.showerror(
            "Database Error",
            "An error occurred while retrieving expense data: " + str(e),
        )


# GUI setup


# GUI setup
root = tk.Tk()
root.title("Expense Tracker")

# Labels
tk.Label(root, text="Category:").grid(row=0, column=0, padx=5, pady=5)
tk.Label(root, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)

# Entry fields
category_entry = tk.Entry(root)
category_entry.grid(row=0, column=1, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=1, column=1, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
clear_button = tk.Button(root, text="Clear Entries", command=clear_entries)
clear_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Show graph button
graph_button = tk.Button(root, text="Show Expense Graph", command=update_graph)
graph_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
