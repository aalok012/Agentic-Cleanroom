import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_1_REQ_2-py"))
import dafny_marshal as M
import F3__1__REQ__2Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine
import json

from app.controllers.f3_1_REQ-1_adapter import AppState

Base.metadata.create_all(engine)

router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_state(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "torrent_sites").first()
    if state_row is None:
        return Dom.Init()
    return M.from_map(json.loads(state_row.value), vconv=str)


def save_state(db: Session, state: Dom.Model):
    json_value = json.dumps(M.from_map(state, vconv=str))
    state_row = db.query(AppState).filter(AppState.key == "torrent_sites").first()
    if state_row is None:
        state_row = AppState(key="torrent_sites", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()


def fr_3_1_REQ_2(request: dict) -> dict:
    with next(get_db_session()) as db:
        model = load_state(db)
        action = core.Action_UpdateSites()
        new_model = Dom.Normalize(Dom.Apply(model, action))
        save_state(db, new_model)
        return {"message": "Database of torrent sites can be updated via the internet."}