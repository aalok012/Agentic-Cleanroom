import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_2_REQ_3-py"))
import dafny_marshal as M
import F3__2__REQ__3Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.extensions import SessionLocal, engine, Base
from sqlalchemy import Column, Integer, String, Text
import json

from app.controllers.f3_2_REQ-10_adapter import AppState

Base.metadata.create_all(engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_state(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        return Dom.Init()
    return M.from_seq(json.loads(state_row.value), lambda x: x)

def save_state(db: Session, state: Dom.Model):
    state_json = json.dumps(M.to_seq(state, lambda x: x))
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        state_row = AppState(key="state", value=state_json)
        db.add(state_row)
    else:
        state_row.value = state_json
    db.commit()

@router.post("/display_error_message")
async def display_error_message(error_type: str, user_action: str, db: Session = Depends(get_db)):
    # Load current state
    model = load_state(db)
    
    # Create action
    action = core.Action_Error()
    
    # Apply action to model
    new_model = Dom.Normalize(Dom.Apply(model, action))
    
    # Save updated state
    save_state(db, new_model)
    
    # Extract message from model
    msg, _ = new_model
    
    return {"error_message": M.from_str(msg)}
