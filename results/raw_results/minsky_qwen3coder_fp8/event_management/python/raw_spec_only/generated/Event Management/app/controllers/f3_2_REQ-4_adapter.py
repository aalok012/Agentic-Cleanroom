import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_2_REQ_4-py"))
import dafny_marshal as M
import F3__2__REQ__4Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine

Base.metadata.create_all(engine)

from app.controllers.f3_2_REQ-10_adapter import AppState

router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fr_3_2_REQ_4(request: dict) -> dict:
    db = next(get_db_session())
    
    # Load existing state or initialize
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row:
        state = M.from_map(Dom.Init(), vconv=str)
        state = M.from_map(state_row.value, vconv=str)
    else:
        state = Dom.Init()
    
    # Convert state to Dafny model
    dafny_state = M.to_map(state, vconv=M.to_str)
    
    # Create action from request
    event_id = request.get("eventId")
    event_name = request.get("eventName")
    
    if not event_id or not event_name:
        raise HTTPException(status_code=400, detail="Missing eventId or eventName")
    
    action = core.Action_PostEvent(M.to_str(event_id), M.to_str(event_name))
    
    # Apply action to state
    new_state = Dom.Normalize(Dom.Apply(dafny_state, action))
    
    # Marshal back to JSON
    json_state = M.from_map(new_state, vconv=M.from_str)
    
    # Save updated state
    if state_row:
        state_row.value = json_state
    else:
        new_row = AppState(key="state", value=json_state)
        db.add(new_row)
    
    db.commit()
    
    return {"message": "Event posted successfully", "eventId": event_id, "eventName": event_name}