from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal
from app.controllers.post_event_on_website import Event

type EventDict = dict[str, str]

router = APIRouter()


def get_ordered_events() -> list[EventDict]:
    """
    An ordered list of events added to the database, sorted in ascending order by their addition timestamp.

    Returns:
        An ordered list of events sorted by addition timestamp
    """
    db = SessionLocal()
    try:
        # Query all events and order them by timestamp
        events = db.query(Event).order_by(Event.timestamp.asc()).all()
        
        # Convert to list of dictionaries
        result = []
        for event in events:
            result.append({
                "id": event.id,
                "timestamp": event.timestamp.isoformat(),
                "description": event.description
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve events")
    finally:
        db.close()