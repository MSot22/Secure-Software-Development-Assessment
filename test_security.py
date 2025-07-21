import os
from encryption import encrypt_file, decrypt_file
from checksum import ChecksumGenerator

def test_encryption_decryption():
    sample = "test.txt"
    with open(sample, "w") as f:
        f.write("secure content")
    encrypted = "test.txt.enc"
    encrypt_file(sample, encrypted)
    decrypted = decrypt_file(encrypted).decode()
    assert decrypted == "secure content"
    os.remove(sample)
    os.remove(encrypted)

def test_checksum():
    with open("check.txt", "w") as f:
        f.write("abc123")
    result = ChecksumGenerator.generate("check.txt")
    assert isinstance(result, str) and len(result) > 10
    os.remove("check.txt")
