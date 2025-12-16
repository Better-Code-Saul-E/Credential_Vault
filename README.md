# Credential Vault

A local first **Command Line Interface Password Manager** built in Python. Designed as a digintal vault for sensitive credentials. It started as a simple JSON-based password manager and evolved step by step into a vault with AES encryption and a master password system.  

---

## Table of Contents
- [Features](#features)
- [Security](#security)
- [Technical Architecture](#technical-architecture)
- [Tech Stack](#tech-stack)

---

## Features
- **AES-256 Encryption**: All data is encrypted using Fernet's symmetric encryption.
- **Session Management**: Supports both "One-Shot" commands and a "Interactive Shell" to reduce repeated password entry.
- **Multi-Vault Support**: Switch between separate vaults (e.g., Default, Work, Personal) to organize credentials.
- **Secure Authentication**: PBKDF2-HMAC-SHA256 salted hashing to verify the master password without storing it.
- **CRUD Operations**: Create, Read, Update, and Delete credentials securely.
- **Smart Utilities**:
  - Clipboard Integration for easy password pasting
  - Password Strength Analyzer evaluating complexity (length, special chars, etc.)
  - Secure Import/Export via encrypted JSON backups

---

## Security
- **Zero-Knowledge Architecture**: The app never stores or sees your master password, only the hash.
- **Salted Hashing**: Unique, random salt for every password to prevent Rainbow Table attacks.
- **Memory Safety**: Fully local, no data is sent to the cloud.
- **Explicit Warnings**: Dangerous actions trigger confirmation prompts (e.g., exporting unencrypted data or using weak passwords).

---

## Technical Architecture
The project follows **MVC Principles** for separation of concern:
- **Models**: Data structures (e.g., Credential objects)
- **Views**: Terminal UI using [Rich](https://github.com/Textualize/rich) for tables, panels, and colored text
- **Controllers**: Coordinate between Views and Services/Repositories
- **Services**: Handle business logic (VaultService, AuthService)
- **Repositories**: Persist encrypted JSON data

---

## Tech Stack
- **Language**: Python 3.10+
- **Cryptography**: `cryptography` library (Fernet/PBKDF2)
- **UI/UX**: `rich` (Terminal formatting), `shlex` (Command parsing)
- **System**: `pyperclip` (Clipboard management), `argparse` (CLI arguments)

