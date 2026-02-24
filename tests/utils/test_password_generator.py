import pytest
import string
from src.vault.utils.password_generator import PasswordGenerator

def test_generate_default_password():
    password = PasswordGenerator.generate()

    assert len(password) == 16
    assert isinstance(password, str)

@pytest.mark.parametrize("length, expected_length", [
    (50, 50),
    (2, 2),
    (0, 0),
    (-10, 0)
])
def test_generate_length(length, expected_length):
    password = PasswordGenerator.generate(length=length)

    assert len(password) == expected_length
    assert isinstance(password, str)

def test_generate_password_wihout_symbols():
    password = PasswordGenerator.generate(length=100 , use_symbols=False)
    
    assert not any(char in string.punctuation for char in password)

def test_generate_password_without_numbers():
    password = PasswordGenerator.generate(length=100 , use_numbers=False)

    assert not any(char.isdigit() for char in password)

def test_generate_password_without_symbols_or_numbers():
    password = PasswordGenerator.generate(use_symbols=False, use_numbers=False)

    assert password.isalpha()

def test_password_generation_uniqueness():
    passwordOne = PasswordGenerator.generate()
    passwordTwo = PasswordGenerator.generate()

    assert passwordOne != passwordTwo