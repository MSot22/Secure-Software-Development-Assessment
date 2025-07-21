import sqlite3
import hashlib
import os

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Connect to database
conn = sqlite3.connect("data/users.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Artefacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        owner TEXT,
        checksum TEXT,
        timestamp_created TEXT,
        timestamp_modified TEXT,
        encrypted_path TEXT
    )
''')

# Create hashed passwords
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# Add admin and user
users = [
    ("admin", hash_pw("admin123"), "admin"),
    ("user", hash_pw("user123"), "user")
]

# Clear old users and insert fresh ones
cursor.execute("DELETE FROM Users")
cursor.executemany("INSERT INTO Users (username, password, role) VALUES (?, ?, ?)", users)

conn.commit()
conn.close()
print("✅ Database reset with admin and user.")
