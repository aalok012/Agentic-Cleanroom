from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal
from app.models._stubs import User

router = APIRouter()

class AuthenticatedUser(Base):
    __tablename__ = "authenticated_users"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    is_enrolled = Column(Boolean, default=False)

@router.post("")
def fr_3_2_REQ_2(request: dict = Body(..., embed=True)) -> dict:
    db = SessionLocal()
    try:
        # Check if the user exists and is enrolled
        user = db.query(User).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if the user is enrolled
        enrolled_user = db.query(AuthenticatedUser).filter_by(user_id=user.id, is_enrolled=True).first()
        if not enrolled_user:
            raise HTTPException(status_code=403, detail="Only enrolled students can register and participate in events")
        
        return {}
    finally:
        db.close()