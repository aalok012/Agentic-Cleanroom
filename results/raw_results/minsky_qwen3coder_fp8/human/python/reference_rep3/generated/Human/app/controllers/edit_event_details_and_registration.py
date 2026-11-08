from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.human.python.reference_rep3.generated.Human.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.human.python.reference_rep3.generated.Human.app.models._stubs import Event

router = APIRouter()

class EventModel(Base):
    __tablename__ = "events"
    __table_args__ = {"extend_existing": True}
    
    event_id = Column(String, primary_key=True)
    title = Column(String)
    date = Column(String)
    location = Column(String)
    age_limit = Column(Integer)
    prerequisites = Column(String)

@router.post("")
def edit_event_details_and_registration(
    event_id: str = Body(..., embed=True),
    details: dict = Body(..., embed=True),
    registration_requirements: dict = Body(..., embed=True)
) -> dict:
    if not event_id:
        raise HTTPException(status_code=400, detail="Event ID cannot be empty")
    
    db = SessionLocal()
    try:
        event = db.query(EventModel).filter(EventModel.event_id == event_id).first()
        
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Update event details
        for key, value in details.items():
            if hasattr(event, key):
                setattr(event, key, value)
        
        # Update registration requirements
        for key, value in registration_requirements.items():
            if hasattr(event, key):
                setattr(event, key, value)
        
        db.commit()
        db.refresh(event)
        
        return {"status": "success", "message": "Event details and registration requirements updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()