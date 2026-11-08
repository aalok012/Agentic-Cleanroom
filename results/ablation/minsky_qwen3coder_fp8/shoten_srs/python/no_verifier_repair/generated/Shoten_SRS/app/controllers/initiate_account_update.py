from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.models.store_user_information import User

router = APIRouter()

def initiate_account_update(user_id: str, update_data: dict) -> None:
    """
    The system accepts the updated account information and begins processing the update.

    Args:
        user_id: Unique identifier for the user whose account is being updated
        update_data: Dictionary containing the updated account information fields

    Returns:
        None.

    Notes:
        Postcondition: The system has received the updated account information and will proceed to validate and apply the changes
    """
    db = SessionLocal()
    try:
        # Retrieve the user by user_id
        user = db.query(User).filter(User.user_id == user_id).first()
        
        # Raise exception if user does not exist
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update user attributes with provided data
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                # Handle unknown fields gracefully or raise an error
                raise HTTPException(status_code=400, detail=f"Invalid field: {key}")
        
        # Commit changes to the database
        db.commit()
    except Exception:
        # Rollback in case of error
        db.rollback()
        raise
    finally:
        # Close the database session
        db.close()