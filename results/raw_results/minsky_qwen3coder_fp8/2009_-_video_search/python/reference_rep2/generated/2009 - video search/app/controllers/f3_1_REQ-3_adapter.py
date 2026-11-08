import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_1_REQ_3-py"))
import dafny_marshal as M
import F3__1__REQ__3Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.extensions import SessionLocal, engine
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class AppState(Base):
    __tablename__ = "app_state"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(Text)

Base.metadata.create_all(engine)

router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_model(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "torrent_search_enabled").first()
    if state_row is None:
        return Dom.Init()
    return M.from_str(state_row.value, lambda x: x)

def save_model(db: Session, model: Dom.Model) -> None:
    json_value = M.to_str(model)
    state_row = db.query(AppState).filter(AppState.key == "torrent_search_enabled").first()
    if state_row is None:
        state_row = AppState(key="torrent_search_enabled", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/configure_torrent_search")
def configure_torrent_search(include_torrents: bool):
    db = next(get_db_session())
    try:
        model = load_model(db)
        action = core.Action_SetTorrentSearchEnabled(include_torrents)
        new_model = Dom.Normalize(Dom.Apply(model, action))
        save_model(db, new_model)
        return {"message": "Torrent search configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))