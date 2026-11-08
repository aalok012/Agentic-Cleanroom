import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_2_REQ_11-py"))
import dafny_marshal as M
import F3__2__REQ__11Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine

Base.metadata.create_all(engine)

router = APIRouter()

from app.controllers.f3_2_REQ-1_adapter import AppState


def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_ordered_events():
    db = next(get_db_session())
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        model = Dom.Init()
    else:
        model = M.from_map(state_row.value, vconv=str)
    
    action = core.Action_GetEvents()
    new_model = Dom.Normalize(Dom.Apply(model, action))
    
    # Convert model to JSON-serializable dict
    json_model = M.from_map(new_model, vconv=str)
    
    # Save updated state
    new_state_json = M.to_map(json_model)
    new_state_str = repr(new_state_json)
    
    if state_row is None:
        new_row = AppState(key="state", value=new_state_str)
        db.add(new_row)
    else:
        state_row.value = new_state_str
    
    db.commit()
    
    # Return the ordered list of events
    result = []
    for k, v in json_model.items():
        result.append({"id": k, "event": v})
    
    # Sort by id to ensure chronological order
    result.sort(key=lambda x: int(x["id"]))
    
    return result