from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal

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

@router.post("")
def post_event_on_website(event_data: dict[str, str | int | list] = Body(..., embed=True)) -> dict[str, str | int]:
    db = SessionLocal()
    try:
        # Generate a unique event ID
        event_id = f"evt_{hash(str(event_data)) % 100000}"
        
        # Create new event instance
        new_event = Event(
            event_id=event_id,
            title=event_data["title"],
            description=event_data["description"],
            date=event_data["date"],
            time=event_data["time"],
            registration_deadline=event_data["registration_deadline"]
        )
        
        # Add to database
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        
        return {"event_id": event_id, "status": "published"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to post event")
    finally:
        db.close()