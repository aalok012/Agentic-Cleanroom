import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_2_REQ_5-py"))
import dafny_marshal as M
import F3__2__REQ__5Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine

# Define the state table
Base = declarative_base()

from app.controllers.f3_2_REQ-10_adapter import AppState

# Create tables
Base.metadata.create_all(engine)

router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_state(db: Session) -> core.Model:
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        return Dom.Init()
    return M.from_map(state_row.value, vconv=str)

def save_state(db: Session, state: core.Model) -> None:
    json_state = M.to_map(state)
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        state_row = AppState(key="state", value=json_state)
        db.add(state_row)
    else:
        state_row.value = json_state
    db.commit()

@router.post("/fr_3_2_REQ_5", response_model=dict)
def fr_3_2_REQ_5(request: dict) -> dict:
    with next(get_db_session()) as db:
        model = load_state(db)
        action = core.Action_GetRegistrants()
        new_state = Dom.Normalize(Dom.Apply(model, action))
        save_state(db, new_state)
        return {"registrants": M.from_map(new_state)}
