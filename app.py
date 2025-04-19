# app.py (Backend)
from flask import Flask, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'dashboard.db'

# Sri Lankan names dataset
SRI_LANKAN_NAMES = [
    "Nimal Perera", "Kamala Silva", "Sunil Fernando", 
    "Priyanka Bandara", "Dinesh Rathnayake", "Anoma Wijesekara",
    "Asanka Gunawardena", "Chamari Athapaththu", "Dilshan Madushanka",
    "Kavisha Dilhari", "Lahiru Kumara", "Malith Perera"
]

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kpis (
                id INTEGER PRIMARY KEY,
                value REAL,
                date TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY,
                total REAL,
                current_week REAL,
                growth REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_name TEXT,
                order_no TEXT,
                amount REAL,
                payment_type TEXT,
                date TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                customer_name TEXT,
                time TEXT,
                amount REAL,
                type TEXT,
                date TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY,
                task TEXT,
                completed BOOLEAN
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY,
                message TEXT,
                time TEXT,
                read BOOLEAN
            )
        ''')
        
        # Insert sample data
        if not cursor.execute("SELECT * FROM kpis").fetchall():
            cursor.executemany("INSERT INTO kpis (value, date) VALUES (?, ?)", [
                (25.0, '2024-08-23'),
                (12.0, '2024-08-24'),
                (3.5, '2024-08-25')
            ])
        
        if not cursor.execute("SELECT * FROM sales").fetchall():
            cursor.execute(
                "INSERT INTO sales (total, current_week, growth) VALUES (?, ?, ?)",
                (3500, 2500, 1.8)
            )
        
        if not cursor.execute("SELECT * FROM orders").fetchall():
            cursor.executemany(
                "INSERT INTO orders (customer_name, order_no, amount, payment_type, date) VALUES (?, ?, ?, ?, ?)",
                [
                    (SRI_LANKAN_NAMES[0], "#790841", 2500, "Credit Card", "2019-02-12"),
                    (SRI_LANKAN_NAMES[1], "#799894", 1500, "PayPal", "2019-02-12"),
                    (SRI_LANKAN_NAMES[2], "#790857", 5600, "Credit Card", "2019-02-12"),
                    (SRI_LANKAN_NAMES[3], "#790687", 2950, "PayPal", "2019-02-12")
                ]
            )
        
        if not cursor.execute("SELECT * FROM transactions").fetchall():
            cursor.executemany(
                "INSERT INTO transactions (customer_name, time, amount, type, date) VALUES (?, ?, ?, ?, ?)",
                [
                    (SRI_LANKAN_NAMES[4], "08:30 AM", -650, "Refund", "2024-08-18"),
                    (SRI_LANKAN_NAMES[5], "09:45 AM", 1400, "Payment", "2024-08-19"),
                    (SRI_LANKAN_NAMES[6], "10:15 AM", 2050, "Payment", "2024-08-20"),
                    (SRI_LANKAN_NAMES[7], "11:30 AM", 650, "Payment", "2024-08-23")
                ]
            )
        
        if not cursor.execute("SELECT * FROM todos").fetchall():
            cursor.executemany(
                "INSERT INTO todos (task, completed) VALUES (?, ?)",
                [
                    ("Review quarterly reports", False),
                    ("Update client database", False),
                    ("Prepare presentation", True),
                    ("Meet with development team", False)
                ]
            )
        
        if not cursor.execute("SELECT * FROM notifications").fetchall():
            cursor.executemany(
                "INSERT INTO notifications (message, time, read) VALUES (?, ?, ?)",
                [
                    ("New order received from " + SRI_LANKAN_NAMES[0], "10:30 AM", False),
                    ("Payment received from " + SRI_LANKAN_NAMES[1], "Yesterday", True),
                    ("System update scheduled", "2 days ago", True)
                ]
            )
        
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/kpis')
def get_kpis():
    try:
        conn = get_db_connection()
        kpis = conn.execute("SELECT value, date FROM kpis").fetchall()
        return jsonify([dict(row) for row in kpis])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/sales')
def get_sales():
    try:
        conn = get_db_connection()
        sales = conn.execute("SELECT total, current_week, growth FROM sales LIMIT 1").fetchone()
        return jsonify(dict(sales)) if sales else jsonify({}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/orders')
def get_orders():
    try:
        conn = get_db_connection()
        orders = conn.execute("SELECT customer_name, order_no, amount, payment_type, date FROM orders").fetchall()
        return jsonify([dict(row) for row in orders])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/transactions')
def get_transactions():
    try:
        conn = get_db_connection()
        transactions = conn.execute("SELECT customer_name, time, amount, type, date FROM transactions").fetchall()
        return jsonify([dict(row) for row in transactions])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/todos')
def get_todos():
    try:
        conn = get_db_connection()
        todos = conn.execute("SELECT id, task, completed FROM todos").fetchall()
        return jsonify([dict(row) for row in todos])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/notifications')
def get_notifications():
    try:
        conn = get_db_connection()
        notifications = conn.execute("SELECT id, message, time, read FROM notifications").fetchall()
        return jsonify([dict(row) for row in notifications])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)