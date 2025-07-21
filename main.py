import os
from auth import login
from db import Database
from encryption import encrypt_file, decrypt_file
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

def list_artefacts(user):
    db = Database.get_instance()
    cursor = db.conn.cursor()
    if user['role'] == 'admin':
        cursor.execute("SELECT * FROM Artefacts")
    else:
        cursor.execute("SELECT * FROM Artefacts WHERE owner = ?", (user['username'],))
    artefacts = cursor.fetchall()

    if not artefacts:
        print("No artefacts found.")
        return

    print("\n--- Artefacts ---")
    for art in artefacts:
        print(f"ID: {art[0]}, File: {art[1]}, Owner: {art[2]}, Created: {art[4]}, Modified: {art[5]}")
    print("-----------------\n")

def update_artefact(user):
    artefact_id = input("Enter artefact ID to update: ")
    new_file_path = input("Enter new file path: ")

    if not os.path.exists(new_file_path):
        print("File not found.")
        return

    db = Database.get_instance()
    cursor = db.conn.cursor()

    cursor.execute("SELECT * FROM Artefacts WHERE id = ?", (artefact_id,))
    art = cursor.fetchone()
    if not art:
        print("Artefact not found.")
        return
    if user['role'] != 'admin' and user['username'] != art[2]:
        print("You don't have permission to update this artefact.")
        return

    encrypted_name = f"data/artefacts/{os.path.basename(new_file_path)}.enc"
    encrypt_file(new_file_path, encrypted_name)
    checksum = ChecksumGenerator.generate(new_file_path)
    modified_time = current_timestamp()

    cursor.execute('''
        UPDATE Artefacts
        SET filename = ?, checksum = ?, timestamp_modified = ?, encrypted_path = ?
        WHERE id = ?''',
        (os.path.basename(new_file_path), checksum, modified_time, encrypted_name, artefact_id)
    )
    db.conn.commit()
    print("Artefact updated.")

def delete_artefact(user):
    artefact_id = input("Enter artefact ID to delete: ")
    db = Database.get_instance()
    cursor = db.conn.cursor()

    if user['role'] != 'admin':
        print("Only admins can delete artefacts.")
        return

    cursor.execute("SELECT * FROM Artefacts WHERE id = ?", (artefact_id,))
    art = cursor.fetchone()
    if not art:
        print("Artefact not found.")
        return

    cursor.execute("DELETE FROM Artefacts WHERE id = ?", (artefact_id,))
    db.conn.commit()
    print("Artefact deleted.")

def main():
    os.makedirs("data/artefacts", exist_ok=True)
    print("Secure Copyright CLI")
    user = login()
    if not user:
        return

    while True:
        print("\nOptions:")
        print("1. Upload Artefact")
        print("2. List Artefacts")
        print("3. Update Artefact")
        if user['role'] == 'admin':
            print("4. Delete Artefact")
            print("5. Exit")
        else:
            print("4. Exit")
        choice = input("Select: ")

        if choice == "1":
            upload_artefact(user)
        elif choice == "2":
            list_artefacts(user)
        elif choice == "3":
            update_artefact(user)
        elif choice == "4" and user['role'] == 'admin':
            delete_artefact(user)
        elif (choice == "4" and user['role'] != 'admin') or (choice == "5" and user['role'] == 'admin'):
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
