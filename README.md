# Credential_Vault

This is my **Credential Vault project in Python**, a command-line tool I built to practice secure storage of usernames and passwords.  It started as a simple JSON-based password manager and evolved step by step into a vault with AES encryption and a master password system.  

## What is does!
- Securely store and manage your credentials (service, username, password)
- Protects your data with a **master password**
- Uses **AES encryption** (via the `cryptography` library) to lock down the vault
- Clean, colorful CLI output with `rich`
- Copy credentials to clipboard with `pyperclip`

### Adding a credential
![Add Credential](images/AddCredential.png)


### Delete a credential
![Add Credential](images/DeleteCredential.png)


### Viewing all credentials
![Add Credential](images/ViewCredentials.png)

