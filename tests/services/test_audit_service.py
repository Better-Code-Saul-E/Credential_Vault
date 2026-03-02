import os
import pytest
from src.vault.services.audit_service import AuditService

@pytest.fixture
def service(tmp_path):
    return AuditService(str(tmp_path))

def test_log_event_creates_and_writes_files(service):
    service.log_event("TEST_ACTION", "This is a test log.")

    assert os.path.exists(service.log_file)
    
    with open(service.log_file, "r") as f:
        assert "TEST_ACTION" in f.readline()

def test_get_parsed_logs_empty_when_no_file(service):
    logs = service.get_parsed_logs()

    assert not logs

def test_get_parsed_logs_reads_correctly(service):
    service.log_event("LOGIN_SUCCESS", "User authenticated")
    logs = service.get_parsed_logs()

    assert len(logs) == 1
    assert logs[0]["action"] == "LOGIN_SUCCESS"

def test_get_parsed_logs_respects_limit(service, tmp_path):
    fake_log_file = tmp_path / "audit.log"

    fake_lines = ""
    for n in range(10):
        fake_lines += f"[2016-03-02 12:00:00] LOGGED_EVENT: Event number {n}\n"
    
    fake_log_file.write_text(fake_lines)
    
    logs = service.get_parsed_logs(8)

    assert len(logs) == 8
    

