from __future__ import annotations

from validators.input_validators import validate_email, validate_password, validate_username


def test_validators_accept_valid_inputs() -> None:
    assert validate_email("hr@example.com") == "hr@example.com"
    assert validate_username("recruiter") == "recruiter"
    assert validate_password("StrongPass1!") == "StrongPass1!"
