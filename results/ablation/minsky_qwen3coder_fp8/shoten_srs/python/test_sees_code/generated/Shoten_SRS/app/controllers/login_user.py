from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.models.store_user_information import User

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
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Assuming password is stored as plain text (not secure, but per spec)
        if user.password != password:
            raise HTTPException(status_code=403, detail="Invalid credentials")
        
        return True
    finally:
        db.close()