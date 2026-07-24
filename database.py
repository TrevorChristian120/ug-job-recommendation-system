import sqlite3

connection = sqlite3.connect("job_recommender.db")

cursor = connection.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    degree TEXT NOT NULL,

    skills TEXT NOT NULL,

    experience TEXT NOT NULL

)
""")

# Skill gaps table
cursor.execute("""
CREATE TABLE IF NOT EXISTS skill_gaps (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    skill TEXT NOT NULL

)
""")

connection.commit()
connection.close()

print("Database Created Successfully")