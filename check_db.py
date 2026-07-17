from database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

print("Students:")
cursor.execute("SELECT * FROM students")
print(cursor.fetchall())

print("\nFace Encodings:")
cursor.execute("SELECT * FROM face_encodings")
print(cursor.fetchall())

print("\nAttendance:")
cursor.execute("SELECT * FROM attendance")
print(cursor.fetchall())

conn.close()