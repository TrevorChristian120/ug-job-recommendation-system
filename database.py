import sqlite3

connection = sqlite3.connect("job_recommender.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    degree TEXT NOT NULL,

    skills TEXT NOT NULL,

    experience TEXT NOT NULL

)
""")

connection.commit()

connection.close()

print("Database Created Successfully")