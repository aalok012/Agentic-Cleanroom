from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal

class Event(Base):
    __tablename__ = "events"
    __table_args__ = {"extend_existing": True}
    
    event_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    location = Column(String, nullable=False)
    registration_details = Column(Text, nullable=False)

router = APIRouter()

@router.post("")
def post_event_on_website(event_data: dict[str, str | int | list] = Body(..., embed=True)) -> dict[str, str | int]:
    db = SessionLocal()
    try:
        # Create a new Event instance with the provided data
        new_event = Event(
            title=event_data["title"],
            description=event_data["description"],
            date=event_data["date"],
            time=event_data["time"],
            location=event_data["location"],
            registration_details=event_data["registration_details"]
        )
        
        # Add the new event to the database
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        
        # Return the event ID and status
        return {"event_id": new_event.event_id, "status": "published"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to post event")
    finally:
        db.close()