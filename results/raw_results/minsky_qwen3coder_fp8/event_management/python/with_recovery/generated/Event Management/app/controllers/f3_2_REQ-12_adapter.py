import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_2_REQ_12-py"))
import dafny_marshal as M
import F3__2__REQ__12Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine
import json

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

def load_state(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        return Dom.Init()
    return M.from_str(state_row.value)


def save_state(db: Session, state: Dom.Model) -> None:
    json_value = M.to_str(state)
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        new_row = AppState(key="state", value=json_value)
        db.add(new_row)
    else:
        state_row.value = json_value
    db.commit()

@router.get("/fr_3_2_REQ_12", status_code=200)
def fr_3_2_REQ_12(db: Session = Depends(get_db_session)):
    # Load current state
    model = load_state(db)
    
    # Apply the action (None in this case)
    action = core.Action_None()
    new_model = Dom.Normalize(Dom.Apply(model, action))
    
    # Save updated state
    save_state(db, new_model)
    
    # Return the new state as JSON
    return {"state": M.from_str(new_model)}