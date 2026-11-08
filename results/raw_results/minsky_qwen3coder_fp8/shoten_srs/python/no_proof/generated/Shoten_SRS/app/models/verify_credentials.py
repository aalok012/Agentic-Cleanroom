from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.models.store_user_information import User

router = APIRouter()

@router.post("")
def verify_credentials(username: str = Body(..., embed=True), password: str = Body(..., embed=True)) -> bool:
    # Check preconditions
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required.")
    
    db = SessionLocal()
    try:
        # Retrieve user from database
        user = db.query(User).filter(User.username == username).first()
        
        # Check if user exists and password matches
        if user and user.password == password:
            # Mark user as logged in
            user.is_logged_in = True
            db.commit()
            return True
        else:
            # Invalid credentials
            return False
    finally:
        db.close()