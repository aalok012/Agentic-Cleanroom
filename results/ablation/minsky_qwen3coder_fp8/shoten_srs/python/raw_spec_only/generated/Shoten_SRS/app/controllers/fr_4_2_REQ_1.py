from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_1_REQ_2 import User

router = APIRouter()

class LoginRequest(Base):
    __tablename__ = "login_requests"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String)

@router.post("")
def fr_4_2_REQ_1(request: dict = Body(..., embed=True)) -> dict:
    db = SessionLocal()
    try:
        # Validate input
        if "username" not in request or "password" not in request:
            raise HTTPException(status_code=400, detail="Username and password are required")
        
        # Check if user exists
        user = db.query(User).filter(User.username == request["username"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify password (assuming password is stored as plain text for simplicity)
        if user.password != request["password"]:
            raise HTTPException(status_code=403, detail="Invalid credentials")
        
        # If we reach here, login is successful
        return {}
    finally:
        db.close()