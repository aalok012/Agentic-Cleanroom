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


def get_ordered_events() -> list[dict[str, str]]:
    db = next(get_db_session())
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        model = Dom.Init()
    else:
        model = M.from_map(state_row.value, vconv=str)
    
    action = core.Action_GetEvents()
    new_model = Dom.Normalize(Dom.Apply(model, action))
    
    # Convert the model to a JSON-serializable format
    json_model = M.to_map(new_model)
    
    # Update the database with the new state
    new_state_row = AppState(key="state", value=json_model)
    db.merge(new_state_row)
    db.commit()
    
    # Return the ordered events as a list of dictionaries
    return [{"id": str(k), "event": v} for k, v in new_model.items()]
