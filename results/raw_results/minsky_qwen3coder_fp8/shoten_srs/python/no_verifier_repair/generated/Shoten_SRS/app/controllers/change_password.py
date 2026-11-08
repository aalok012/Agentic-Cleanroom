from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.models.store_user_information import User

router = APIRouter()

def change_password(user_id: str, old_password: str, new_password: str, confirm_new_password: str) -> bool:
    """
    The system updates the user's password to the new one provided.

    Args:
        user_id: Unique identifier for the user changing their password
        old_password: The user's current password
        new_password: The new password the user wants to set
        confirm_new_password: The new password confirmed by the user

    Returns:
        Boolean indicating whether the password change was successful

    Raises:
        HTTPException: If the precondition is violated (The old password provided matches the currently stored password for the user).

    Notes:
        Precondition: The old password provided matches the currently stored password for the user
        Postcondition: The user's password is replaced with the new password, provided both new password entries match and the old password was correct
    """
    db = SessionLocal()
    try:
        # Find the user by user_id
        user = db.query(User).filter(User.user_id == user_id).first()
        
        # Check if user exists
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify old password
        if user.password != old_password:
            raise HTTPException(status_code=400, detail="Old password is incorrect")
        
        # Check if new passwords match
        if new_password != confirm_new_password:
            raise HTTPException(status_code=400, detail="New passwords do not match")
        
        # Update the password
        user.password = new_password
        db.commit()
        
        return True
    finally:
        db.close()