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
