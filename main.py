# main.py
from database import create_tables
from book import add_book, view_all_books, search_book, delete_book
from member import add_member, view_all_members, search_member, delete_member
from transaction import issue_book, return_book, view_transactions, member_history
from dsa_utils import binary_search_book, BookHashMap, TransactionStack

# =================== ADMIN LOGIN ===================
def admin_login():
    print("\n" + "=" * 40)
    print("   🔐 SMART LIBRARY MANAGEMENT SYSTEM")
    print("=" * 40)

    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "library123"

    attempts = 3

    while attempts > 0:
        print(f"\n🔑 Login ({attempts} attempts left)")
        username = input("Username: ")
        password = input("Password: ")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            print("\n✅ Login successful! Welcome Admin! 👋")
            return True
        else:
            attempts -= 1
            if attempts > 0:
                print(f"❌ Wrong credentials! {attempts} attempts left.")
            else:
                print("🚫 Too many failed attempts! System locked.")
                return False

# =================== BOOK MENU ===================
def book_menu():
    while True:
        print("\n📚 BOOK MANAGEMENT")
        print("-" * 30)
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Delete Book")
        print("5. Binary Search by ID (DSA)")
        print("0. Back to Main Menu")
        print("-" * 30)

        choice = input("Choose: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            view_all_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            delete_book()
        elif choice == "5":
            book_id = int(input("Enter Book ID: "))
            binary_search_book(book_id)
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice!")

# =================== MEMBER MENU ===================
def member_menu():
    while True:
        print("\n👤 MEMBER MANAGEMENT")
        print("-" * 30)
        print("1. Register Member")
        print("2. View All Members")
        print("3. Search Member")
        print("4. Delete Member")
        print("0. Back to Main Menu")
        print("-" * 30)

        choice = input("Choose: ")

        if choice == "1":
            add_member()
        elif choice == "2":
            view_all_members()
        elif choice == "3":
            search_member()
        elif choice == "4":
            delete_member()
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice!")

# =================== TRANSACTION MENU ===================
def transaction_menu():
    while True:
        print("\n💳 TRANSACTION MANAGEMENT")
        print("-" * 30)
        print("1. Issue Book")
        print("2. Return Book")
        print("3. View All Transactions")
        print("4. Member History")
        print("0. Back to Main Menu")
        print("-" * 30)

        choice = input("Choose: ")

        if choice == "1":
            issue_book()
        elif choice == "2":
            return_book()
        elif choice == "3":
            view_transactions()
        elif choice == "4":
            member_history()
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice!")

# =================== DSA MENU ===================
def dsa_menu():
    while True:
        print("\n🧠 DSA UTILITIES")
        print("-" * 30)
        print("1. Binary Search (Find Book by ID)")
        print("2. HashMap (All Books Fast Lookup)")
        print("3. Stack (Recent Transactions)")
        print("0. Back to Main Menu")
        print("-" * 30)

        choice = input("Choose: ")

        if choice == "1":
            book_id = int(input("Enter Book ID: "))
            binary_search_book(book_id)
        elif choice == "2":
            hm = BookHashMap()
            hm.load_books()
            hm.display_all()
        elif choice == "3":
            stack = TransactionStack()
            stack.load_from_db()
            stack.display()
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice!")

# =================== REPORTS MENU ===================
def reports_menu():
    while True:
        print("\n📊 REPORTS & ANALYTICS")
        print("-" * 30)
        print("1. Export Transaction Report (.txt)")
        print("2. Most Issued Book")
        print("3. Library Statistics")
        print("0. Back to Main Menu")
        print("-" * 30)

        choice = input("Choose: ")

        if choice == "1":
            export_report()
        elif choice == "2":
            most_issued_book()
        elif choice == "3":
            library_stats()
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice!")

# =================== EXPORT REPORT ===================
def export_report():
    from database import get_connection
    from datetime import datetime

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

    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w") as f:
        f.write("=" * 65 + "\n")
        f.write("      SMART LIBRARY MANAGEMENT SYSTEM - REPORT\n")
        f.write(f"      Generated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
        f.write("=" * 65 + "\n\n")
        f.write(f"{'ID':<5} {'Member':<15} {'Book':<20} {'Issued':<12} {'Returned':<12} {'Fine':<6} {'Status'}\n")
        f.write("-" * 65 + "\n")

        for r in records:
            returned = r[4] if r[4] else "---"
            f.write(f"{r[0]:<5} {r[1]:<15} {r[2]:<20} {r[3]:<12} {returned:<12} Rs{r[5]:<5} {r[6]}\n")

        f.write("-" * 65 + "\n")
        f.write(f"\nTotal Transactions: {len(records)}\n")

    print(f"✅ Report saved as '{filename}' in Library_System folder!")

# =================== MOST ISSUED BOOK ===================
def most_issued_book():
    from database import get_connection

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT b.title, b.author, COUNT(t.book_id) as issue_count
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        GROUP BY t.book_id
        ORDER BY issue_count DESC
        LIMIT 5
    ''')
    results = cursor.fetchall()
    conn.close()

    if not results:
        print("❌ No transactions found!")
        return

    print("\n📈 MOST ISSUED BOOKS (Top 5):")
    print("-" * 45)
    print(f"{'Rank':<6} {'Title':<25} {'Author':<15} {'Times'}")
    print("-" * 45)
    for i, r in enumerate(results, 1):
        print(f"{i:<6} {r[0]:<25} {r[1]:<15} {r[2]}")
    print("-" * 45)

# =================== LIBRARY STATS ===================
def library_stats():
    from database import get_connection

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(available_copies) FROM books")
    available = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM members")
    total_members = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions WHERE status = 'issued'")
    currently_issued = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(fine) FROM transactions")
    total_fine = cursor.fetchone()[0] or 0

    conn.close()

    print("\n📊 LIBRARY STATISTICS:")
    print("=" * 35)
    print(f"  📚 Total Books       : {total_books}")
    print(f"  ✅ Available Books   : {available}")
    print(f"  📤 Currently Issued  : {currently_issued}")
    print(f"  👤 Total Members     : {total_members}")
    print(f"  💰 Total Fine Collected: Rs{total_fine}")
    print("=" * 35)

# =================== MAIN MENU ===================
def main():
    create_tables()

    if not admin_login():
        return

    while True:
        print("\n" + "=" * 40)
        print("   📖 SMART LIBRARY MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. 📚 Book Management")
        print("2. 👤 Member Management")
        print("3. 💳 Transaction Management")
        print("4. 🧠 DSA Utilities")
        print("5. 📊 Reports & Analytics")
        print("0. 🚪 Exit")
        print("=" * 40)

        choice = input("Choose: ")

        if choice == "1":
            book_menu()
        elif choice == "2":
            member_menu()
        elif choice == "3":
            transaction_menu()
        elif choice == "4":
            dsa_menu()
        elif choice == "5":
            reports_menu()
        elif choice == "0":
            print("\n👋 Thank you! Library System closed.")
            break
        else:
            print("❌ Invalid choice! Try again.")

# =================== RUN ===================
if __name__ == "__main__":
    main()