import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_2_REQ_10-py"))
import dafny_marshal as M
import F3__2__REQ__10Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import SessionLocal, Session

from app.extensions import Base, SessionLocal, engine

router = APIRouter()

class AppState(Base):
    __tablename__ = "app_state"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(Text)

Base.metadata.create_all(engine)

def append_event(event_data: dict[str, str]) -> None:
    db: Session = SessionLocal()
    try:
        # Load existing state or initialize to empty
        state_row = db.query(AppState).filter(AppState.key == "state").first()
        if state_row:
            state = M.from_map(state_row.value, vconv=str)
        else:
            state = Dom.Init()
        
        # Convert event_data to Dafny map
        event_map = M.to_map(event_data)
        
        # Extract eventId and eventData from the map
        # Since we're appending one event at a time, we'll take the first key-value pair
        # This assumes event_data is a single key-value pair
        event_id = next(iter(event_map))
        event_data_value = event_map[event_id]
        
        # Create the action
        action = core.Action_AppendEvent(M.to_str(event_id), M.to_str(event_data_value))
        
        # Apply the action to the state
        new_state = Dom.Normalize(Dom.Apply(state, action))
        
        # Marshal back to JSON
        json_state = M.to_map(new_state, kconv=M.to_str, vconv=M.to_str)
        
        # Save back to DB
        if state_row:
            state_row.value = json_state
        else:
            new_row = AppState(key="state", value=json_state)
            db.add(new_row)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to append event: {str(e)}")
    finally:
        db.close()