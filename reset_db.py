from database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("DELETE FROM students")
cursor.execute("DELETE FROM face_encodings")
cursor.execute("DELETE FROM attendance")

conn.commit()
conn.close()

print("Database reset complete")