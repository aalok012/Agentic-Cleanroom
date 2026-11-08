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

from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine
import json

from app.controllers.f3_2_REQ-1_adapter import AppState

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
    return M.from_seq(json.loads(state_row.value), lambda x: x)

def save_state(db: Session, state: Dom.Model) -> None:
    json_value = json.dumps(M.to_seq(state, lambda x: x))
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        state_row = AppState(key="state", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/display_error_message")
def display_error_message(error_type: str, details: str):
    with next(get_db_session()) as db:
        model = load_state(db)
        action = core.Action_Error()
        new_model = Dom.Normalize(Dom.Apply(model, action))
        save_state(db, new_model)
        
        # Extract the error message from the model
        msg, _ = new_model
        return {"message": msg}