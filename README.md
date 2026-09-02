# 🔐 File Encryption and Decryption Tool

A secure web-based application for encrypting and decrypting files using modern cryptographic techniques.

## 📌 Project Overview

The File Encryption and Decryption Tool is a cybersecurity project designed to protect sensitive files from unauthorized access.

The application allows users to select a file, enter a password, and securely encrypt or decrypt the file.

## ✨ Features

- 🔐 Secure file encryption
- 🔓 File decryption using the correct password
- 🛡️ AES-GCM authenticated encryption
- 🔑 Password-based key derivation using PBKDF2
- 👁️ Password visibility toggle
- 📁 Supports file-based encryption and decryption
- 💻 Simple and user-friendly web interface
- ✅ Integrity verification using authentication

## 🛠️ Technologies Used

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask
- PyCryptodome

### Cryptography
- AES-GCM
- PBKDF2-HMAC-SHA256
- SHA-256
- Random salt and nonce generation

## 🔒 Security

The application uses:

- *AES-GCM* for authenticated encryption
- *PBKDF2-HMAC-SHA256* for deriving a secure encryption key from the user's password
- A randomly generated *salt* for each encryption operation
- A randomly generated *nonce* for AES-GCM
- Authentication tag verification to detect incorrect passwords or modified encrypted data

## ⚙️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/aswinkumarcos-pixel/File-Encryption-And-Decryption-Tool.git
