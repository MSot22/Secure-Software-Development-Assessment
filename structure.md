secure-copyright-cli/
├── main.py                 # CLI entry point
├── auth.py                 # Login + hashing logic
├── db.py                   # Singleton DB + DAO pattern
├── encryption.py           # File encryption/decryption
├── checksum.py             # Checksum generation (SHA-256)
├── timestamp.py            # Timestamp utility
├── setup_database.py       # DB setup script
├── requirements.txt
├── data/
│   ├── artefacts/          # Encrypted artefacts
│   └── users.db            # SQLite database
└── tests/
    └── test_security.py    # Unit tests
