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

from app.controllers.f3_2_REQ-10_adapter import AppState


def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_ordered_events() -> list[dict[str, str]]:
    db = next(get_db_session())
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        state = Dom.Init()
    else:
        state = M.from_map(state_row.value, vconv=int)
    
    action = core.Action_GetEvents()
    new_state = Dom.Normalize(Dom.Apply(state, action))
    
    # Convert the model to a JSON-serializable format
    result = M.from_map(new_state, vconv=str)
    
    # Serialize the new state back to the database
    serialized_state = M.to_map(new_state)
    state_json = M.from_map(serialized_state, vconv=str)
    
    if state_row is None:
        new_row = AppState(key="state", value=state_json)
        db.add(new_row)
    else:
        state_row.value = state_json
    
    db.commit()
    
    # Return the ordered list of events
    return [{"key": k, "value": str(v)} for k, v in sorted(result.items())]
