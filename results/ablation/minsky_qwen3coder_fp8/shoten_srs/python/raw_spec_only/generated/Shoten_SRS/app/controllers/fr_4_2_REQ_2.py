from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal


from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_1_REQ_2 import User


router = APIRouter()


def fr_4_2_REQ_2(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Validate that username and password are present in the request
        if "username" not in request or "password" not in request:
            raise HTTPException(status_code=400, detail="Username and password are required.")
        
        # Check if the user exists in the database
        user = db.query(User).filter(User.username == request["username"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        # Verify the password (in a real application, you would hash and compare)
        if user.password != request["password"]:
            raise HTTPException(status_code=403, detail="Incorrect password.")
        
        # Return success response
        return {}
    finally:
        db.close()