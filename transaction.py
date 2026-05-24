# transaction.py
from database import get_connection
from datetime import datetime, date

# =================== ISSUE BOOK ===================
def issue_book():
    print("\n📤 ISSUE BOOK TO MEMBER")

    member_id = int(input("Enter Member ID: "))
    book_id = int(input("Enter Book ID: "))

    conn = get_connection()
    cursor = conn.cursor()

    # Check member exists
    cursor.execute("SELECT * FROM members WHERE member_id = ?", (member_id,))
    member = cursor.fetchone()
    if not member:
        print("❌ Member not found!")
        conn.close()
        return

    # Check book exists
    cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
    book = cursor.fetchone()
    if not book:
        print("❌ Book not found!")
        conn.close()
        return

    # Check available copies
    if book[4] <= 0:
        print("❌ No copies available right now!")
        conn.close()
        return

    # Check if same member already issued same book
    cursor.execute('''
        SELECT * FROM transactions
        WHERE member_id = ? AND book_id = ? AND status = 'issued'
    ''', (member_id, book_id))
    already = cursor.fetchone()
    if already:
        print("❌ This member already has this book issued!")
        conn.close()
        return

    # Issue the book
    issue_date = date.today().strftime("%Y-%m-%d")
    cursor.execute('''
        INSERT INTO transactions (member_id, book_id, issue_date, status)
        VALUES (?, ?, ?, 'issued')
    ''', (member_id, book_id, issue_date))

    # Reduce available copies
    cursor.execute('''
        UPDATE books SET available_copies = available_copies - 1
        WHERE book_id = ?
    ''', (book_id,))

    conn.commit()
    conn.close()
    print(f"✅ Book '{book[1]}' issued to '{member[1]}' on {issue_date}")
    print("📅 Please return within 14 days to avoid fine!")

# =================== RETURN BOOK ===================
def return_book():
    print("\n📥 RETURN BOOK")

    member_id = int(input("Enter Member ID: "))
    book_id = int(input("Enter Book ID: "))

    conn = get_connection()
    cursor = conn.cursor()

    # Find active transaction
    cursor.execute('''
        SELECT * FROM transactions
        WHERE member_id = ? AND book_id = ? AND status = 'issued'
    ''', (member_id, book_id))
    txn = cursor.fetchone()

    if not txn:
        print("❌ No active transaction found for this member and book!")
        conn.close()
        return

    # Calculate fine
    issue_date = datetime.strptime(txn[3], "%Y-%m-%d").date()
    return_date = date.today()
    days = (return_date - issue_date).days
    fine = 0

    if days > 14:
        extra_days = days - 14
        fine = extra_days * 2  # ₹2 per extra day
        print(f"⚠️  Book returned after {days} days!")
        print(f"💰 Fine: ₹{fine} ({extra_days} extra days × ₹2)")
    else:
        print(f"✅ Book returned on time! ({days} days)")

    return_date_str = return_date.strftime("%Y-%m-%d")

    # Update transaction
    cursor.execute('''
        UPDATE transactions
        SET return_date = ?, fine = ?, status = 'returned'
        WHERE txn_id = ?
    ''', (return_date_str, fine, txn[0]))

    # Increase available copies
    cursor.execute('''
        UPDATE books SET available_copies = available_copies + 1
        WHERE book_id = ?
    ''', (book_id,))

    conn.commit()
    conn.close()
    print(f"📚 Book returned successfully on {return_date_str}")

# =================== VIEW ALL TRANSACTIONS ===================
def view_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT t.txn_id, m.name, b.title, t.issue_date,
               t.return_date, t.fine, t.status
        FROM transactions t
        JOIN members m ON t.member_id = m.member_id
        JOIN books b ON t.book_id = b.book_id
        ORDER BY t.txn_id DESC
    ''')
    records = cursor.fetchall()
    conn.close()

    if not records:
        print("\n❌ No transactions found!")
        return

    print("\n📋 ALL TRANSACTIONS:")
    print("-" * 80)
    print(f"{'ID':<5} {'Member':<15} {'Book':<20} {'Issued':<12} {'Returned':<12} {'Fine':<6} {'Status'}")
    print("-" * 80)
    for r in records:
        returned = r[4] if r[4] else "---"
        print(f"{r[0]:<5} {r[1]:<15} {r[2]:<20} {r[3]:<12} {returned:<12} ₹{r[5]:<5} {r[6]}")
    print("-" * 80)

# =================== VIEW MEMBER HISTORY ===================
def member_history():
    member_id = int(input("\nEnter Member ID to see history: "))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT t.txn_id, b.title, t.issue_date,
               t.return_date, t.fine, t.status
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        WHERE t.member_id = ?
        ORDER BY t.txn_id DESC
    ''', (member_id,))
    records = cursor.fetchall()
    conn.close()

    if not records:
        print("❌ No history found for this member!")
        return

    print(f"\n📖 TRANSACTION HISTORY (Member ID: {member_id})")
    print("-" * 70)
    print(f"{'TxnID':<7} {'Book':<22} {'Issued':<12} {'Returned':<12} {'Fine':<6} {'Status'}")
    print("-" * 70)
    for r in records:
        returned = r[3] if r[3] else "---"
        print(f"{r[0]:<7} {r[1]:<22} {r[2]:<12} {returned:<12} ₹{r[4]:<5} {r[5]}")
    print("-" * 70)

# =================== TEST ===================
if __name__ == "__main__":
    from database import create_tables
    create_tables()
    print("1. Issue Book")
    print("2. Return Book")
    print("3. View All Transactions")
    choice = input("Choose: ")
    if choice == "1":
        issue_book()
    elif choice == "2":
        return_book()
    elif choice == "3":
        view_transactions()