import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_2_REQ_1-py"))
import dafny_marshal as M
import F3__2__REQ__1Domain as core
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_state(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "feature_state").first()
    if state_row is None:
        return Dom.Init()
    return M.from_str(state_row.value)

def save_state(db: Session, model: Dom.Model):
    json_value = M.to_str(model)
    state_row = db.query(AppState).filter(AppState.key == "feature_state").first()
    if state_row is None:
        state_row = AppState(key="feature_state", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/check_internet_access", response_model=bool)
def check_internet_access(db: Session = Depends(get_db)) -> bool:
    # Load current state
    state = load_state(db)
    
    # Build action
    action = core.Action_Access()
    
    # Apply action to state
    new_state = Dom.Normalize(Dom.Apply(state, action))
    
    # Save updated state
    save_state(db, new_state)
    
    # Return result
    return True