import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_1_REQ_1-py"))
import dafny_marshal as M
import F3__1__REQ__1Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine
import json

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

def load_state(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        return Dom.Init()
    return M.from_json(state_row.value, Dom.Model)

def save_state(db: Session, model: Dom.Model) -> None:
    json_value = M.to_json(model)
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        state_row = AppState(key="state", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/search-torrents-and-streaming")
def search_torrents_and_streaming(query: str):
    with next(get_db_session()) as db:
        model = load_state(db)
        action = core.Action_Search(M.to_str(query))
        new_model = Dom.Normalize(Dom.Apply(model, action))
        save_state(db, new_model)
        
        # Extract the query from the new model for the response
        query_result = M.from_str(new_model[0])
        
        # Return the result as per the contract
        return {"query": query_result, "torrents": [], "streams": []}