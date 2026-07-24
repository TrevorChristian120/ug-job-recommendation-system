import sqlite3

connection = sqlite3.connect(
    "job_recommender.db"
)

cursor = connection.cursor()

cursor.execute(
    "SELECT * FROM users"
)

rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()