import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_1_REQ_5-py"))
import dafny_marshal as M
import F3__1__REQ__5Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.extensions import SessionLocal, engine
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from app.controllers.f3_1_REQ-1_adapter import AppState

Base.metadata.create_all(engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_state(db: Session, key: str):
    state_row = db.query(AppState).filter(AppState.key == key).first()
    if state_row is None:
        return Dom.Init()
    else:
        return M.from_str(state_row.value)

def save_state(db: Session, key: str, state):
    json_value = M.to_str(state)
    state_row = db.query(AppState).filter(AppState.key == key).first()
    if state_row is None:
        new_row = AppState(key=key, value=json_value)
        db.add(new_row)
    else:
        state_row.value = json_value
    db.commit()

@router.get("/search", response_model=str)
def handle_search_results(query: str, db: Session = Depends(get_db)):
    # Load the current state
    model = load_state(db, "search_state")
    
    # Create the action
    action = core.Action_SearchNoMatch()
    
    # Apply the action to the model
    new_state = Dom.Normalize(Dom.Apply(model, action))
    
    # Save the new state
    save_state(db, "search_state", new_state)
    
    # Return the result
    return new_state