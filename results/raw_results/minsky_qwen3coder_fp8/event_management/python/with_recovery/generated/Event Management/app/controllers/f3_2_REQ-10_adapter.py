import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_2_REQ_10-py"))
import dafny_marshal as M
import F3__2__REQ__10Domain as core
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

def load_model(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        return Dom.Init()
    return M.from_map(json.loads(state_row.value), vconv=str)

def save_model(db: Session, model: Dom.Model) -> None:
    json_value = json.dumps(M.from_map(model, vconv=str))
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        new_row = AppState(key="state", value=json_value)
        db.add(new_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/event")
def append_event(event_data: dict[str, str]):
    with next(get_db_session()) as db:
        model = load_model(db)
        # Convert event_data to Dafny map
        event_map = M.to_map(event_data, kconv=M.to_str, vconv=M.to_str)
        
        # Create action for each key-value pair
        for key, value in event_map.items():
            action = core.Action_AppendEvent(M.from_str(key), M.from_str(value))
            model = Dom.Normalize(Dom.Apply(model, action))
        
        save_model(db, model)
        return {"status": "success"}