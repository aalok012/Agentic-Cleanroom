from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal

from app.controllers.post_event_on_website import Event

router = APIRouter()


def append_event(event_data: dict[str, str]) -> None:
    """The event is successfully added to the database."""
    db = SessionLocal()
    try:
        event = Event(
            title=event_data["title"],
            description=event_data["description"]
        )
        db.add(event)
        db.commit()
        db.refresh(event)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to add event to database")
    finally:
        db.close()