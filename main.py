import os
from auth import login
from db import Database
from encryption import encrypt_file
from checksum import ChecksumGenerator
from timestamp import current_timestamp

def upload_artefact(user):
    file_path = input("Enter path to artefact: ")
    if not os.path.exists(file_path):
        print("File not found.")
        return

    encrypted_name = f"data/artefacts/{os.path.basename(file_path)}.enc"
    encrypt_file(file_path, encrypted_name)

    checksum = ChecksumGenerator.generate(file_path)
    timestamp = current_timestamp()

    db = Database.get_instance()
    db.save_artefact((os.path.basename(file_path), user['username'], checksum, timestamp, timestamp, encrypted_name))
    print("Artefact uploaded and encrypted successfully.")

def main():
    print("Secure Copyright CLI")
    user = login()
    if not user:
        return

    while True:
        print("\n1. Upload Artefact\n2. Exit")
        choice = input("Select: ")
        if choice == "1":
            upload_artefact(user)
        elif choice == "2":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
