from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_1_REQ_2 import User

router = APIRouter()

@router.post("")
def fr_4_2_REQ_3(request: dict = Body(..., embed=True)) -> dict:
    db = SessionLocal()
    try:
        # Extract username and password from request
        username = request.get("username")
        password = request.get("password")
        
        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password are required.")
        
        # Find user in the database
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        # Verify password (in a real app, you'd hash and compare)
        if user.password != password:
            raise HTTPException(status_code=403, detail="Invalid credentials.")
        
        # Mark user as logged in
        user.is_logged_in = True
        db.commit()
        
        # Return empty dict on success
        return {}
    finally:
        db.close()