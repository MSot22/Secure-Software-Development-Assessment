import hashlib
import getpass
from db import Database

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    db = Database.get_instance()
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    user = db.get_user(username)
    if user and user[2] == hash_password(password):
        print(f"Login successful. Welcome, {username} ({user[3]})!")
        return {"username": username, "role": user[3]}
    else:
        print("Invalid credentials.")
        return None
