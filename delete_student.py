from database.db import get_connection

student_id = input("Enter Student ID to delete: ")

conn = get_connection()
cursor = conn.cursor()

try:

    cursor.execute("""
    DELETE FROM attendance
    WHERE student_id = ?
    """, (student_id,))

    cursor.execute("""
    DELETE FROM face_encodings
    WHERE student_id = ?
    """, (student_id,))

    cursor.execute("""
    DELETE FROM students
    WHERE student_id = ?
    """, (student_id,))

    conn.commit()

    print("Student deleted successfully.")

except Exception as e:

    print("Error:", e)

finally:

    conn.close()