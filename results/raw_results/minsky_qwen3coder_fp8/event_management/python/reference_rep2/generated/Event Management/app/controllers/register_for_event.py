from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal
from app.models._stubs import User
from app.models.post_event_on_website import Event

class Registration(Base):
    __tablename__ = "registrations"
    __table_args__ = {"extend_existing": True}
    user_id = Column(String, primary_key=True)
    event_id = Column(String, primary_key=True)

router = APIRouter()

@router.post("")
def register_for_event(user_id: str = Body(..., embed=True), event_id: str = Body(..., embed=True)) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if user exists and is authenticated and enrolled
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if user is enrolled (assuming enrolled students have a flag)
        if not user.is_enrolled:
            raise HTTPException(status_code=403, detail="User is not enrolled as a student")
        
        # Check if event exists
        event = db.query(Event).filter(Event.event_id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Create registration
        registration = Registration(user_id=user_id, event_id=event_id)
        db.add(registration)
        db.commit()
        
        return {"status": "registered", "user_id": user_id, "event_id": event_id}
    finally:
        db.close()