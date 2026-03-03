import sqlite3

conn = sqlite3.connect("documents.db")
cursor = conn.cursor()

for row in cursor.execute("SELECT * FROM documents"):
    print(row)

conn.close()