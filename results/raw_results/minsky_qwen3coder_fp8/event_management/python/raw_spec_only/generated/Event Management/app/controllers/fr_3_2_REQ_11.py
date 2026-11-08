from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal

class Event(Base):
    __tablename__ = "events"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    timestamp = Column(Float)
    is_active = Column(Boolean)

router = APIRouter()

@router.post("")
def fr_3_2_REQ_11(request: dict = Body(..., embed=True)) -> dict:
    db = SessionLocal()
    try:
        # Query all events ordered by timestamp
        events = db.query(Event).order_by(Event.timestamp).all()
        
        # Prepare the response list
        result = []
        for event in events:
            result.append({
                "id": event.id,
                "name": event.name,
                "description": event.description,
                "timestamp": event.timestamp,
                "is_active": event.is_active
            })
        
        return {"events": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()