from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.models.store_user_information import User

type User = dict[str, object]

router = APIRouter()


def login_user(username: str, password: str) -> bool:
    """
    The system grants access to the user's account if the credentials are valid.

    Args:
        username: The username provided by the user for login.
        password: The password provided by the user for login.

    Returns:
        True if the credentials are valid and the user is authenticated, False otherwise.

    Notes:
        Postcondition: The user is authenticated and allowed to proceed with account-related activities.
    """
    db = SessionLocal()
    try:
        # Query the user by username
        user = db.query(User).filter(User.username == username).first()
        
        # Check if user exists and password matches
        if user and user.password == password:
            return True
        else:
            raise HTTPException(status_code=403, detail="Invalid credentials")
    finally:
        db.close()