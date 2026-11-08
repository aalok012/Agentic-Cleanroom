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
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine
import json

# Ensure the table exists
Base.metadata.create_all(engine)

from app.controllers.f3_1_REQ-3_adapter import AppState

router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_state(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "search_state").first()
    if state_row is None:
        return Dom.Init()
    return M.from_str(state_row.value)


def save_state(db: Session, model: Dom.Model) -> None:
    json_value = M.to_str(model)
    state_row = db.query(AppState).filter(AppState.key == "search_state").first()
    if state_row is None:
        new_row = AppState(key="search_state", value=json_value)
        db.add(new_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/search", response_model=str)
def handle_search_results(query: str):
    with next(get_db_session()) as db:
        model = load_state(db)
        action = core.Action_SearchNoMatch()
        new_model = Dom.Normalize(Dom.Apply(model, action))
        save_state(db, new_model)
        return M.from_str(new_model)