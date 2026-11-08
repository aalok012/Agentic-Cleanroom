from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

router = APIRouter()

@router.post("")
def check_admin_access(user_credentials: dict[str, str] = Body(..., embed=True)) -> bool:
    db = SessionLocal()
    try:
        # Validate preconditions
        if not user_credentials.get("username") or not user_credentials.get("password"):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        # Query the user from the database
        user = db.query(User).filter(User.username == user_credentials["username"]).first()
        
        # Check if user exists and password matches
        if not user or user.password != user_credentials["password"]:
            raise HTTPException(status_code=403, detail="Access denied: Invalid credentials or insufficient permissions")
        
        # Check if user has admin privileges
        if not user.is_admin:
            raise HTTPException(status_code=403, detail="Access denied: Insufficient permissions")
        
        return True
    finally:
        db.close()