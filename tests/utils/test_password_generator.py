import pytest
import string
from src.vault.utils.password_generator import PasswordGenerator

def test_generate_default_password():
    password = PasswordGenerator.generate()

    assert len(password) == 16
    assert isinstance(password, str)

@pytest.mark.parametrize("length", [
    3,
    16,
    50
])
def test_generate_length(length):
    password = PasswordGenerator.generate(length=length)

    assert len(password) == length
    assert isinstance(password, str)

@pytest.mark.parametrize("length", [
    2, 
    0, 
    -10
])
def test_generate_raises_error_on_impossible_constraints(length):
        with pytest.raises(ValueError, match="too short"):
            PasswordGenerator.generate(length=length)

@pytest.mark.parametrize("use_symbols, use_numbers", [
    (True, True),  
    (True, False),  
    (False, True),  
    (False, False)  
])
def test_generate_character_constraints(use_symbols, use_numbers):
    password = PasswordGenerator.generate(length=20, use_symbols=use_symbols, use_numbers=use_numbers)
    
    has_symbols = any(char in string.punctuation for char in password)
    has_numbers = any(char.isdigit() for char in password)
    
    assert has_symbols == use_symbols
    assert has_numbers == use_numbers

def test_password_generation_uniqueness():
    passwordOne = PasswordGenerator.generate()
    passwordTwo = PasswordGenerator.generate()

    assert passwordOne != passwordTwo