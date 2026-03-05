import pytest
from unittest.mock import Mock
from src.vault.services.authentication_service import AuthenticationService


@pytest.fixture
def auth_service():
    mock_repo = Mock()
    mock_hasher = Mock()

    return AuthenticationService(mock_repo, mock_hasher)

def test_create_master_hash_success(auth_service):
    auth_service.repo.save_hash.return_value = True
    auth_service.hasher.hash_password.return_value = "scrambled_fake_hash"

    result = auth_service.create_master_hash("my_password")

    assert result
    auth_service.hasher.hash_password.assert_called_with("my_password") 
    auth_service.repo.save_hash.assert_called_with("scrambled_fake_hash")

def test_verify_password_success(auth_service):
    auth_service.repo.load_hash.return_value = "saved_hash_from_file"
    auth_service.hasher.verify_password.return_value = True

    verified = auth_service.verify_password("fake_password")

    assert verified
    auth_service.hasher.verify_password.assert_called_with("fake_password", "saved_hash_from_file")

def test_verify_password_fails_when_no_hash_exists(auth_service):
    auth_service.repo.load_hash.return_value = None

    verified = auth_service.verify_password("fake_password")

    assert not verified
    auth_service.hasher.verify_password.assert_not_called()


