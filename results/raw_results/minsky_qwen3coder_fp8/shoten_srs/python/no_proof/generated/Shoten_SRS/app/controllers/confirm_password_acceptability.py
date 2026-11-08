from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class PasswordValidation(Base):
    __tablename__ = "password_validations"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    password = Column(String, nullable=False)
    is_acceptable = Column(Boolean, nullable=False)

router = APIRouter()


def confirm_password_acceptability(password: str) -> bool:
    """
    The system confirms whether the password meets the security requirements.

    Args:
        password: Password provided by the user

    Returns:
        The system confirms whether the password meets the security requirements

    Raises:
        HTTPException: If the precondition is violated (The user has been prompted to enter a password).

    Notes:
        Precondition: The user has been prompted to enter a password
        Postcondition: The system verifies that the entered password satisfies the defined criteria for acceptability
        canonical call (must work): {"password":"SecurePass123!"}
        must return on success: true
        error_mode: raise

        precondition failure call (must raise HTTPException with a 4xx status): {"password":"weakpass"}
    """
    if not password:
        raise HTTPException(status_code=400, detail="The user has been prompted to enter a password.")

    # Check if password meets security requirements
    # At least 8 characters, contains uppercase, lowercase, digit, and special character
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    is_long_enough = len(password) >= 8

    is_acceptable = all([is_long_enough, has_upper, has_lower, has_digit, has_special])

    db = SessionLocal()
    try:
        # Store validation result in DB
        validation = PasswordValidation(password=password, is_acceptable=is_acceptable)
        db.add(validation)
        db.commit()
        db.refresh(validation)
    finally:
        db.close()

    return is_acceptable