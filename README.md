# Secure Copyright Management CLI Application

## Description
A secure Python command-line application to manage music artefacts (lyrics, MP3s, scores) using:
- AES encryption
- SHA-256 checksums
- Timestamps
- Role-based access control (Admin/User)

---

## Features
- Upload, view, update, and delete encrypted artefacts
- Admins can manage all artefacts; users can only manage their own
- All files are stored encrypted with a checksum and timestamp

---

## Roles
- **Admin**
  - Upload / View / Update / Delete any artefact
- **User**
  - Upload / View / Update only own artefacts

---

## How to Run

1. Install dependencies:
2. Run the app:

---

## Default Users (preloaded)

| Role  | Username | Password  |
|-------|----------|-----------|
| Admin | admin    | admin123  |
| User  | user     | user123   |

---

## Testing

Run unit tests:
