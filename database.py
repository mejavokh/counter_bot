import sqlite3
from datetime import datetime


def create_connection():
    connect = sqlite3.connect('expenses.db')
    return connect


def create_table():
    connect = create_connection()
    cursor = connect.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    date TEXT 
    )
    ''')
    connect.commit()
    connect.close()


def add_expense(user_id, amount):
    connect = create_connection()
    cursor = connect.cursor()
    cursor.execute('''
    INSERT INTO expenses (user_id, amount, date)
    VALUES (?,?,?)
    ''', (user_id, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    connect.commit()
    connect.close()


def get_expenses(user_id, period):
    connect = create_connection()
    cursor = connect.cursor()

    if period == 'day':
        cursor.execute('''
        SELECT SUM(amount) FROM expenses 
        WHERE user_id = ? AND date(date) = date('now')
        ''', (user_id,))
    elif period == 'week':
        cursor.execute('''
        SELECT SUM(amount) FROM expenses
         WHERE user_id = ? AND date(date) >= date('now', '-7 days')
        ''', (user_id,))
    elif period == 'month':
        cursor.execute('''
        SELECT SUM(amount) FROM expenses
         WHERE user_id = ? AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        ''', (user_id,))
    elif period == 'year':
        cursor.execute('''
        SELECT SUM(amount) FROM expenses
         WHERE user_id = ? AND strftime('%Y', date) = strftime('%Y', 'now')
        ''', (user_id, ))

    result = cursor.fetchone()
    connect.close()
    return result[0] if result[0] else 0.0



