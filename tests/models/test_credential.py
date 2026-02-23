import pytest
from dataclasses import asdict
from src.vault.models.credential import Credential

def test_credential_initialization():
    cred = Credential("Facebook", "Mark", "Zukerberg1")

    assert cred.service_name == "Facebook"
    assert cred.username == "Mark"
    assert cred.password == "Zukerberg1"

def test_credential_to_dict():
    cred = Credential("Facebook", "Mark", "Zukerberg1")

    assert asdict(cred) == {
        "service_name": "Facebook",
        "username": "Mark",
        "password": "Zukerberg1"
    }