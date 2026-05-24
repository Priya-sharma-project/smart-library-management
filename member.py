# member.py
from database import get_connection

# =================== ADD MEMBER ===================
def add_member():
    print("\n👤 REGISTER NEW MEMBER")
    name = input("Member Name: ")
    email = input("Email Address: ")
    phone = input("Phone Number: ")

    conn = get_connection()
    cursor = conn.cursor()

    # Check if email already exists
    cursor.execute("SELECT * FROM members WHERE email = ?", (email,))
    existing = cursor.fetchone()

    if existing:
        print("❌ Member with this email already exists!")
        conn.close()
        return

    cursor.execute('''
        INSERT INTO members (name, email, phone)
        VALUES (?, ?, ?)
    ''', (name, email, phone))

    conn.commit()
    conn.close()
    print(f"✅ Member '{name}' registered successfully!")

# =================== VIEW ALL MEMBERS ===================
def view_all_members():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    conn.close()

    if not members:
        print("\n❌ No members found!")
        return

    print("\n👥 ALL MEMBERS:")
    print("-" * 65)
    print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'Phone'}")
    print("-" * 65)
    for m in members:
        print(f"{m[0]:<5} {m[1]:<20} {m[2]:<25} {m[3]}")
    print("-" * 65)

# =================== SEARCH MEMBER ===================
def search_member():
    print("\n🔍 SEARCH MEMBER")
    keyword = input("Enter name or email to search: ").lower()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM members
        WHERE LOWER(name) LIKE ? OR LOWER(email) LIKE ?
    ''', (f'%{keyword}%', f'%{keyword}%'))

    results = cursor.fetchall()
    conn.close()

    if not results:
        print("❌ No member found!")
        return

    print(f"\n✅ {len(results)} member(s) found:")
    print("-" * 65)
    print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'Phone'}")
    print("-" * 65)
    for m in results:
        print(f"{m[0]:<5} {m[1]:<20} {m[2]:<25} {m[3]}")
    print("-" * 65)

# =================== DELETE MEMBER ===================
def delete_member():
    print("\n🗑️ DELETE MEMBER")
    view_all_members()
    member_id = int(input("\nEnter Member ID to delete: "))

    conn = get_connection()
    cursor = conn.cursor()

    # Check if member has active issued books
    cursor.execute('''
        SELECT * FROM transactions
        WHERE member_id = ? AND status = 'issued'
    ''', (member_id,))
    active = cursor.fetchone()

    if active:
        print("❌ Cannot delete! This member has books currently issued.")
        conn.close()
        return

    cursor.execute("DELETE FROM members WHERE member_id = ?", (member_id,))
    conn.commit()
    conn.close()
    print("✅ Member deleted successfully!")

# =================== GET MEMBER BY ID (helper) ===================
def get_member_by_id(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE member_id = ?", (member_id,))
    member = cursor.fetchone()
    conn.close()
    return member

# =================== TEST ===================
if __name__ == "__main__":
    from database import create_tables
    create_tables()
    add_member()
    view_all_members()