import sqlite3
import os

# Create db directory if it doesn't exist
os.makedirs("db", exist_ok=True)

conn = sqlite3.connect("db/users.db")

cursor = conn.cursor()

TABLE_NAME = "users"
cursor.execute(f"""
  CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
               id INTEGER PRIMARY KEY,
               name TEXT,
               email TEXT)
  """)

USERS = [
  (1, "Sandip", "sgahlot@somewhere.com"),
  (2, "Mikhail", "mkhail@somewhere.com"),
  (3, "Jeremy", "jeremy@somewhere.com"),
  (4, "Chris", "chris@somewhere.com"),
]

cursor.executemany(
  f"""
    INSERT OR REPLACE INTO {TABLE_NAME}(id, name, email)
                   VALUES(?, ?, ?)
  """,
  USERS,
)

conn.commit()
print(f"{len(USERS)} {TABLE_NAME} inserted...")

cursor.execute(f"SELECT * FROM {TABLE_NAME}")
rows = cursor.fetchall()
for row in rows:
  print(f" -> {row}")

conn.close()
