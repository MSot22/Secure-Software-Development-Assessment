from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    return open(KEY_FILE, "rb").read()

def encrypt_file(file_path, output_path):
    generate_key()
    key = load_key()
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted = fernet.encrypt(file.read())
    with open(output_path, "wb") as enc_file:
        enc_file.write(encrypted)

def decrypt_file(encrypted_path):
    key = load_key()
    fernet = Fernet(key)
    with open(encrypted_path, "rb") as enc_file:
        return fernet.decrypt(enc_file.read())
