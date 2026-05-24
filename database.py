# database.py
import sqlite3

def get_connection():
    conn = sqlite3.connect("library.db")
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Books table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            total_copies INTEGER DEFAULT 1,
            available_copies INTEGER DEFAULT 1
        )
    ''')

    # Members table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT
        )
    ''')

    # Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            book_id INTEGER,
            issue_date TEXT,
            return_date TEXT,
            fine REAL DEFAULT 0,
            status TEXT DEFAULT 'issued',
            FOREIGN KEY(member_id) REFERENCES members(member_id),
            FOREIGN KEY(book_id) REFERENCES books(book_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database ready!")

# Run this to test
if __name__ == "__main__":
    create_tables()