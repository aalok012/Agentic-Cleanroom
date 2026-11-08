from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_1_REQ_2 import User

router = APIRouter()

@router.post("")
def fr_4_11_REQ_3(request: dict = Body(..., embed=True)) -> dict:
    db = SessionLocal()
    try:
        # Extract fields from request
        old_password = request.get("old_password")
        new_password = request.get("new_password")
        confirm_new_password = request.get("confirm_new_password")
        
        # Validate inputs
        if not old_password or not new_password or not confirm_new_password:
            raise HTTPException(status_code=400, detail="All password fields are required.")
        
        if new_password != confirm_new_password:
            raise HTTPException(status_code=400, detail="New passwords do not match.")
        
        # For demonstration purposes, we'll assume a hardcoded user ID
        # In real implementation, this would come from authentication context
        user_id = 1
        
        # Fetch user from DB
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        # Check if old password matches
        if user.password != old_password:
            raise HTTPException(status_code=400, detail="Old password is incorrect.")
        
        # Update password
        user.password = new_password
        db.commit()
        
        return {}
    finally:
        db.close()