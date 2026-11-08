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

def load_state(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        return Dom.Init()
    return M.from_map(json.loads(state_row.value), vconv=str)

def save_state(db: Session, state: Dom.Model) -> None:
    json_value = json.dumps(M.from_map(state, vconv=str))
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        new_row = AppState(key="state", value=json_value)
        db.add(new_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/generate_registrant_list", response_model=list[dict[str, str]])
def generate_registrant_list():
    with next(get_db_session()) as db:
        model = load_state(db)
        action = core.Action_GenerateList()
        new_state = Dom.Normalize(Dom.Apply(model, action))
        save_state(db, new_state)
        return M.from_map(new_state, vconv=str)