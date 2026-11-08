import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_2_REQ_6-py"))
import dafny_marshal as M
import F3__2__REQ__6Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException, Request
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
    return M.from_map(json.loads(state_row.value), vconv=M.from_map)


def save_state(db: Session, state: Dom.Model) -> None:
    json_value = json.dumps(M.from_map(state, vconv=lambda x: M.from_map(x, vconv=str)))
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        new_row = AppState(key="state", value=json_value)
        db.add(new_row)
    else:
        state_row.value = json_value
    db.commit()

@router.get("/stakeholder-database")
def stakeholder_database():
    db = next(get_db_session())
    state = load_state(db)
    return M.from_map(state, vconv=M.from_map)
