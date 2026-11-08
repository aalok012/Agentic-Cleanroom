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

# Define the state table
Base = declarative_base()

from app.controllers.f3_1_REQ-1_adapter import AppState

# Create tables
Base.metadata.create_all(engine)

router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_model(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        return Dom.Init()
    return M.from_map(json.loads(state_row.value), vconv=str)

def save_model(db: Session, model: Dom.Model) -> None:
    json_value = json.dumps(M.from_map(model, vconv=str))
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        new_row = AppState(key="model", value=json_value)
        db.add(new_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/torrent-sites/update", response_model=bool)
def update_torrent_sites_database():
    db = next(get_db_session())
    try:
        model = load_model(db)
        action = core.Action_UpdateDB()
        new_model = Dom.Normalize(Dom.Apply(model, action))
        save_model(db, new_model)
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update torrent sites database: {str(e)}")