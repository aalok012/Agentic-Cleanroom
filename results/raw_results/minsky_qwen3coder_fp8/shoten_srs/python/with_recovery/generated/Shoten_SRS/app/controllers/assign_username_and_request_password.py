from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.extensions import Base, SessionLocal


from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.models.store_user_information import User


router = APIRouter()


def assign_username_and_request_password() -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if all required information has been collected
        # For this implementation, we assume that the user has already provided all required info
        
        # Generate a username (simplified logic - in reality this would be more complex)
        username = "johndoe123"  # This should come from actual logic
        
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # In a real implementation, we would save the username to the database
        # For now, we're just returning the username as requested
        
        return {"username": username}
    finally:
        db.close()