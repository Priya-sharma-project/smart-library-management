# dsa_utils.py
from database import get_connection

# =================== DSA 1: BINARY SEARCH ===================
# Books ko ID se dhundhna - sorted list mein fast search

def binary_search_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books ORDER BY book_id")
    books = cursor.fetchall()
    conn.close()

    if not books:
        print("❌ No books in database!")
        return None

    low = 0
    high = len(books) - 1

    while low <= high:
        mid = (low + high) // 2
        if books[mid][0] == book_id:
            print(f"\n✅ Book found using Binary Search!")
            print(f"   ID     : {books[mid][0]}")
            print(f"   Title  : {books[mid][1]}")
            print(f"   Author : {books[mid][2]}")
            print(f"   Total  : {books[mid][3]}")
            print(f"   Avail  : {books[mid][4]}")
            return books[mid]
        elif books[mid][0] < book_id:
            low = mid + 1
        else:
            high = mid - 1

    print(f"❌ Book with ID {book_id} not found!")
    return None


# =================== DSA 2: STACK ===================
# Last 10 transactions ka history stack mein store hoga

class TransactionStack:
    def __init__(self):
        self.stack = []
        self.max_size = 10

    def push(self, transaction):
        if len(self.stack) >= self.max_size:
            self.stack.pop(0)  # purana remove karo
        self.stack.append(transaction)

    def pop(self):
        if self.is_empty():
            print("❌ Stack is empty!")
            return None
        return self.stack.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0

    def display(self):
        if self.is_empty():
            print("❌ No recent transactions!")
            return

        print("\n📚 RECENT TRANSACTIONS (Stack - Latest First):")
        print("-" * 55)
        print(f"{'TxnID':<7} {'Member':<18} {'Book':<18} {'Status'}")
        print("-" * 55)
        for txn in reversed(self.stack):
            print(f"{txn[0]:<7} {txn[1]:<18} {txn[2]:<18} {txn[3]}")
        print("-" * 55)

    def load_from_db(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT t.txn_id, m.name, b.title, t.status
            FROM transactions t
            JOIN members m ON t.member_id = m.member_id
            JOIN books b ON t.book_id = b.book_id
            ORDER BY t.txn_id DESC
            LIMIT 10
        ''')
        records = cursor.fetchall()
        conn.close()

        self.stack = list(reversed(records))
        print("✅ Transaction stack loaded from database!")


# =================== DSA 3: HASH MAP ===================
# Books ko fast access ke liye dictionary mein store karna

class BookHashMap:
    def __init__(self):
        self.hashmap = {}  # key: book_id, value: book data

    def load_books(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        conn.close()

        for book in books:
            self.hashmap[book[0]] = {
                "id"    : book[0],
                "title" : book[1],
                "author": book[2],
                "total" : book[3],
                "avail" : book[4]
            }
        print(f"✅ {len(self.hashmap)} books loaded into HashMap!")

    def get_book(self, book_id):
        if book_id in self.hashmap:
            book = self.hashmap[book_id]
            print(f"\n⚡ Book found using HashMap (O(1) speed)!")
            print(f"   ID     : {book['id']}")
            print(f"   Title  : {book['title']}")
            print(f"   Author : {book['author']}")
            print(f"   Total  : {book['total']}")
            print(f"   Avail  : {book['avail']}")
            return book
        else:
            print(f"❌ Book ID {book_id} not found in HashMap!")
            return None

    def display_all(self):
        if not self.hashmap:
            print("❌ HashMap is empty!")
            return
        print(f"\n🗂️  HASHMAP - All Books ({len(self.hashmap)} total):")
        print("-" * 55)
        for key, book in self.hashmap.items():
            print(f"Key:{key} → {book['title']} | {book['author']} | Avail:{book['avail']}")
        print("-" * 55)


# =================== TEST ===================
if __name__ == "__main__":
    from database import create_tables
    create_tables()

    print("\n🔍 Testing Binary Search:")
    book_id = int(input("Enter Book ID to search: "))
    binary_search_book(book_id)

    print("\n📦 Testing HashMap:")
    hm = BookHashMap()
    hm.load_books()
    hm.display_all()

    print("\n📋 Testing Stack:")
    stack = TransactionStack()
    stack.load_from_db()
    stack.display()