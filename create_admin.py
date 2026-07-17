from database.db import get_connection
from werkzeug.security import generate_password_hash

def create_admin():
    conn = get_connection()
    cursor = conn.cursor()

    username = "admin"
    password = "admin123"
    email = "admin@example.com"

    password_hash = generate_password_hash(password)

    cursor.execute("""
    INSERT INTO admins (username, password_hash, email)
    VALUES (?, ?, ?)
    """, (username, password_hash, email))

    conn.commit()
    conn.close()

    print("Admin created successfully.")

create_admin()