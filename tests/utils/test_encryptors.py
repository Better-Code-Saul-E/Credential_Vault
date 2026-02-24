import pytest
from src.vault.utils.encryptors import Pbkdf2PasswordHasher, FernetDataEncryptor
from cryptography.fernet import InvalidToken

@pytest.fixture
def hasher():
    return Pbkdf2PasswordHasher()

@pytest.fixture
def encryptor():
    return FernetDataEncryptor()

def test_correct_password(hasher):
    password = "MasterPassword10!"
    hashed_password = hasher.hash_password(password)

    assert hasher.verify_password(password, hashed_password)

def test_incorrect_password(hasher):
    password = "MasterPassword10!"
    wrong_password = "WrongPassword"
    hashed_password = hasher.hash_password(password)

    assert hasher.verify_password(wrong_password, hashed_password) is False

def test_corrupted_hex(hasher):
    password = "MasterPassword10!"
    corrupted_hex = "10snglak85n1olkmcn0119u4n"

    assert hasher.verify_password(password, corrupted_hex) is False

def test_hash_uniqueness(hasher):
    password = "MasterPassword10!"

    hash_one = hasher.hash_password(password)
    hash_two = hasher.hash_password(password)

    assert hash_one != hash_two

def test_password_decryption(encryptor):
    data = '{"Netflix": {"username": "saul", "password": "password123"} }'
    password = "MasterPassword10!"

    encrypted_data = encryptor.encrypt(data, password)

    assert encryptor.decrypt(encrypted_data, password) == data

def test_encryption_uniqueness(encryptor):
    data = '{"Netflix": {"username": "saul", "password": "password123"} }'
    password = "MasterPassword10!"

    first_encryption = encryptor.encrypt(data, password)
    second_encryption = encryptor.encrypt(data, password)

    assert first_encryption != second_encryption

def test_decrypt_wrong_password(encryptor):
    data = '{"Netflix": {"username": "saul", "password": "password123"} }'
    password = "MasterPassword10!"
    wrong_password = "WrongPassword10!"

    encrypted_data = encryptor.encrypt(data, password)

    with pytest.raises(InvalidToken):
        encryptor.decrypt(encrypted_data, wrong_password)
