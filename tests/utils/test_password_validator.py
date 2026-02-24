import pytest
from src.vault.utils.password_validator import PasswordStrength


@pytest.mark.parametrize("password, expected_score, expected_feedback", [
    ("password", 1, ["Add numbers", "Mix uppercase & lowercase", "Add special chars (@, #, $, etc.)", "Avoid common passwords"]),
    ("JavaSuks101!", 5, []),
    ("C00KIEs", 3, ["Too short (min 8 chars)", "Add special chars (@, #, $, etc.)"]),
    ("t0ast1", 2, ["Too short (min 8 chars)", "Mix uppercase & lowercase", "Add special chars (@, #, $, etc.)"]),
    ("$uperr1ch", 4, ["Mix uppercase & lowercase"])
])
def test_validate_password_requirments(password, expected_score, expected_feedback):
    validator = PasswordStrength()

    score, feedback = validator.validate_password(password)

    assert feedback == expected_feedback
    assert score == expected_score

@pytest.mark.parametrize("score, feedback, expected_format", [
    (4, ["Mix uppercase & lowercase"], "[bold green]STRONG[/bold green]"),
    (2, ["Too short (min 8 chars)", "Mix uppercase & lowercase", "Add special chars (@, #, $, etc.)"], "[bold yellow]MEDIUM[/bold yellow]"),
    (1, ["Too short (min 8 chars)", "Add special chars (@, #, $, etc.)"], "[bold red]WEAK[/bold red] (Too short (min 8 chars), Add special chars (@, #, $, etc.))")
])
def test_format_password_strength(score, feedback, expected_format):
    validator = PasswordStrength()
    
    formatted_result = validator.format_password_strength(score, feedback)

    assert formatted_result == expected_format



