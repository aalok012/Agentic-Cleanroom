from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal
import uuid

class Event(Base):
    __tablename__ = "events"
    __table_args__ = {"extend_existing": True}
    
    event_id = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    date = Column(String)
    time = Column(String)
    registration_deadline = Column(String)

router = APIRouter()

def validate_event_data(event_data: dict[str, str | int | list]) -> None:
    if "title" not in event_data or not event_data["title"]:
        raise HTTPException(status_code=400, detail="Title is required")
    
    if "description" not in event_data or not event_data["description"]:
        raise HTTPException(status_code=400, detail="Description is required")
    
    if "date" not in event_data or not event_data["date"]:
        raise HTTPException(status_code=400, detail="Date is required")
    
    if "time" not in event_data or not event_data["time"]:
        raise HTTPException(status_code=400, detail="Time is required")
    
    if "registration_deadline" not in event_data or not event_data["registration_deadline"]:
        raise HTTPException(status_code=400, detail="Registration deadline is required")

@router.post("")
def post_event_on_website(event_data: dict[str, str | int | list] = Body(..., embed=True)) -> dict[str, str | int]:
    validate_event_data(event_data)
    
    db = SessionLocal()
    try:
        # Generate a unique event ID
        event_id = f"evt_{uuid.uuid4().hex[:8]}"
        
        # Create a new event instance
        event = Event(
            event_id=event_id,
            title=event_data["title"],
            description=event_data["description"],
            date=event_data["date"],
            time=event_data["time"],
            registration_deadline=event_data["registration_deadline"]
        )
        
        # Add and commit the event to the database
        db.add(event)
        db.commit()
        db.refresh(event)
        
        # Return the event ID and status
        return {"event_id": event.event_id, "status": "published"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to post event")
    finally:
        db.close()