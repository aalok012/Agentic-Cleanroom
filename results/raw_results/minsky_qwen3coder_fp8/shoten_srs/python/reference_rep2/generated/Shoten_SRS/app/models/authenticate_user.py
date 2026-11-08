from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.models.store_user_information import User

router = APIRouter()


def authenticate_user(username: str, password: str) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if username and password are provided
        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password are required.")
        
        # Validate credentials using the prerequisite functions
        from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.controllers.login_user import login_user
        from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.controllers.validate_login_credentials import validate_login_credentials
        
        # Run the prerequisites
        login_user_result = login_user(username=username, password=password)
        validate_result = validate_login_credentials(username=username, password=password)
        
        # If either prerequisite fails, raise an exception
        if not login_user_result or not validate_result:
            raise HTTPException(status_code=400, detail="Invalid credentials.")
        
        # Find the user in the database
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        # Mark the user as logged in
        user.is_logged_in = True
        db.commit()
        db.refresh(user)
        
        # Return session token and user ID
        return {"session_token": "abc123xyz", "user_id": str(user.id)}
    finally:
        db.close()