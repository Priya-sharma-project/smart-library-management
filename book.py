# book.py
from database import get_connection

# =================== ADD BOOK ===================
def add_book():
    print("\n📚 ADD NEW BOOK")
    title = input("Book Title: ")
    author = input("Author Name: ")
    copies = int(input("Total Copies: "))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO books (title, author, total_copies, available_copies)
        VALUES (?, ?, ?, ?)
    ''', (title, author, copies, copies))

    conn.commit()
    conn.close()
    print(f"✅ Book '{title}' added successfully!")

# =================== VIEW ALL BOOKS ===================
def view_all_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()

    if not books:
        print("\n❌ No books found!")
        return

    # DSA - Merge Sort (by title alphabetically)
    sorted_books = merge_sort(list(books))

    print("\n📋 ALL BOOKS (Sorted A-Z by Title):")
    print("-" * 65)
    print(f"{'ID':<5} {'Title':<25} {'Author':<20} {'Total':<7} {'Avail'}")
    print("-" * 65)
    for book in sorted_books:
        print(f"{book[0]:<5} {book[1]:<25} {book[2]:<20} {book[3]:<7} {book[4]}")
    print("-" * 65)

# =================== SEARCH BOOK ===================
def search_book():
    print("\n🔍 SEARCH BOOK")
    keyword = input("Enter title or author to search: ").lower()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM books
        WHERE LOWER(title) LIKE ? OR LOWER(author) LIKE ?
    ''', (f'%{keyword}%', f'%{keyword}%'))

    results = cursor.fetchall()
    conn.close()

    if not results:
        print("❌ No book found with that keyword!")
        return

    print(f"\n✅ {len(results)} book(s) found:")
    print("-" * 65)
    print(f"{'ID':<5} {'Title':<25} {'Author':<20} {'Total':<7} {'Avail'}")
    print("-" * 65)
    for book in results:
        print(f"{book[0]:<5} {book[1]:<25} {book[2]:<20} {book[3]:<7} {book[4]}")
    print("-" * 65)

# =================== DELETE BOOK ===================
def delete_book():
    print("\n🗑️ DELETE BOOK")
    view_all_books()
    book_id = int(input("\nEnter Book ID to delete: "))

    conn = get_connection()
    cursor = conn.cursor()

    # Check if book is currently issued
    cursor.execute('''
        SELECT * FROM transactions
        WHERE book_id = ? AND status = 'issued'
    ''', (book_id,))
    active = cursor.fetchone()

    if active:
        print("❌ Cannot delete! This book is currently issued to a member.")
        conn.close()
        return

    cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
    conn.commit()
    conn.close()
    print("✅ Book deleted successfully!")

# =================== DSA - MERGE SORT ===================
def merge_sort(books):
    if len(books) <= 1:
        return books

    mid = len(books) // 2
    left = merge_sort(books[:mid])
    right = merge_sort(books[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        # Compare titles (index 1) alphabetically
        if left[i][1].lower() <= right[j][1].lower():
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# =================== TEST ===================
if __name__ == "__main__":
    from database import create_tables
    create_tables()
    add_book()
    view_all_books()