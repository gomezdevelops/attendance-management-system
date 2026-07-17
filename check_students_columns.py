from database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(students)")

columns = cursor.fetchall()

for col in columns:
    print(col)

conn.close()