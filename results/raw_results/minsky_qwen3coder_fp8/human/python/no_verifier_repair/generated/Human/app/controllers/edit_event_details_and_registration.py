from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.human.python.no_verifier_repair.generated.Human.app.extensions import Base, SessionLocal

class Event(Base):
    __tablename__ = "events"
    __table_args__ = {"extend_existing": True}
    
    event_id = Column(String, primary_key=True)
    title = Column(String)
    description = Column(Text)
    date = Column(String)
    age_limit = Column(Integer)
    prerequisites = Column(String)
    
router = APIRouter()

@router.post("")
def edit_event_details_and_registration(
    event_id: str = Body(..., embed=True),
    details: dict = Body(..., embed=True),
    registration_requirements: dict = Body(..., embed=True)
) -> bool:
    db = SessionLocal()
    try:
        # Retrieve the event from the database
        event = db.query(Event).filter(Event.event_id == event_id).first()
        
        # Check if event exists
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Update event details
        if "title" in details:
            event.title = details["title"]
        if "description" in details:
            event.description = details["description"]
        if "date" in details:
            event.date = details["date"]
        
        # Update registration requirements
        if "age_limit" in registration_requirements:
            event.age_limit = registration_requirements["age_limit"]
        if "prerequisites" in registration_requirements:
            event.prerequisites = registration_requirements["prerequisites"]
        
        # Commit changes to the database
        db.commit()
        
        return True
    except Exception as e:
        # Rollback in case of error
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()