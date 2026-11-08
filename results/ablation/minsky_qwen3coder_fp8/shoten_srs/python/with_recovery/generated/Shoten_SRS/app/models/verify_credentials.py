from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.models.store_user_information import User

def verify_credentials(username: str, password: str) -> bool:
    """
    The system confirms the validity of the credentials and marks the user as logged-in.

    Args:
        username: The username provided by the user for login.
        password: The password provided by the user for login.

    Returns:
        True if the credentials are valid and the user is authenticated, False otherwise.

    Raises:
        HTTPException: If the precondition is violated (The username and password are provided by the user.).
    """
    # Check preconditions
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required.")
    
    db = SessionLocal()
    try:
        # Retrieve the user from the database
        user = db.query(User).filter(User.username == username).first()
        
        # Check if user exists and password matches
        if user and user.password == password:
            # Mark the user as logged in
            user.is_logged_in = True
            db.commit()
            return True
        else:
            return False
    finally:
        db.close()