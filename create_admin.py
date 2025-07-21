import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("data/users.db")
cursor = conn.cursor()
username = "admin"
password = "admin123"
role = "admin"

hashed_pw = hash_password(password)

cursor.execute("DELETE FROM Users WHERE username = ?", (username,))
cursor.execute("INSERT INTO Users (username, password, role) VALUES (?, ?, ?)",
               (username, hashed_pw, role))

conn.commit()
conn.close()
print("Admin user created.")
