from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.human.python.raw_spec_only.generated.Human.app.extensions import Base, SessionLocal


class Event(Base):
    __tablename__ = "events"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    registration_requirements = Column(String)


router = APIRouter()


def fr_3_1_REQ_1(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Assuming the request contains event_id and updated fields
        event_id = request.get("event_id")
        if not event_id:
            raise HTTPException(status_code=400, detail="Event ID is required.")

        # Fetch the event from the database
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found.")

        # Update event details if provided
        if "title" in request:
            event.title = request["title"]
        if "description" in request:
            event.description = request["description"]
        if "registration_requirements" in request:
            event.registration_requirements = request["registration_requirements"]

        # Commit changes to the database
        db.commit()
        db.refresh(event)

        return {}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()