import sqlite3
from sqlite3 import Error

class Database:
    _instance = None

    def __init__(self):
        if Database._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.conn = self.create_connection()
            self.create_tables()
            Database._instance = self

    @staticmethod
    def get_instance():
        if Database._instance is None:
            Database()
        return Database._instance

    def create_connection(self):
        try:
            conn = sqlite3.connect("data/users.db")
            return conn
        except Error as e:
            print(e)

    def create_tables(self):
        cursor = self.conn.cursor()
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
        self.conn.commit()

    def add_user(self, username, password_hash, role):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Users (username, password, role) VALUES (?, ?, ?)",
                       (username, password_hash, role))
        self.conn.commit()

    def get_user(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        return cursor.fetchone()

    def save_artefact(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO Artefacts (filename, owner, checksum, timestamp_created, timestamp_modified, encrypted_path)
            VALUES (?, ?, ?, ?, ?, ?)''', data)
        self.conn.commit()
