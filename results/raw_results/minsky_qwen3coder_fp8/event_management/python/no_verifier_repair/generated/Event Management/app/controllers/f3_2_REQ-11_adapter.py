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

import json

from app.controllers.f3_2_REQ-10_adapter import AppState

Base.metadata.create_all(engine)

router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_model(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        return Dom.Init()
    else:
        return M.from_map(json.loads(state_row.value), vconv=int)

def set_model(db: Session, model: Dom.Model) -> None:
    json_value = json.dumps(M.from_map(model, vconv=str))
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        new_row = AppState(key="model", value=json_value)
        db.add(new_row)
    else:
        state_row.value = json_value
    db.commit()

@router.get("/ordered-events", response_model=list[dict[str, str]])
def get_ordered_events():
    db = next(get_db_session())
    model = get_model(db)
    action = core.Action_GetEvents()
    new_state = Dom.Normalize(Dom.Apply(model, action))
    
    # Convert the model to a list of events
    events_list = []
    for key in sorted(new_state.keys()):
        events_list.append({"event": key, "timestamp": str(new_state[key])})
    
    set_model(db, new_state)
    return events_list