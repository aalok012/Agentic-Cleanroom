from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal
from app.models._stubs import User
from app.controllers.post_event_on_website import Event

class Registration(Base):
    __tablename__ = "registrations"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    event_id = Column(String, index=True)

router = APIRouter()

@router.post("")
def register_for_event(user_id: str = Body(..., embed=True), event_id: str = Body(..., embed=True)) -> bool:
    db = SessionLocal()
    try:
        # Check if user exists and is authenticated (enrolled student)
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_enrolled:
            raise HTTPException(status_code=403, detail="User is not authenticated or enrolled as a student")
        
        # Check if event exists
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Check if user is already registered for the event
        existing_registration = db.query(Registration).filter(
            Registration.user_id == user_id,
            Registration.event_id == event_id
        ).first()
        if existing_registration:
            return True  # Already registered, consider successful
        
        # Create new registration
        new_registration = Registration(user_id=user_id, event_id=event_id)
        db.add(new_registration)
        db.commit()
        db.refresh(new_registration)
        
        return True
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()