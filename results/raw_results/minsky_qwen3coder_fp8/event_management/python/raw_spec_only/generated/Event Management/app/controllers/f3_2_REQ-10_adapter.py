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
    return M.from_map(json.loads(state_row.value), vconv=M.from_str)

def save_model(db: Session, model: Dom.Model):
    json_value = json.dumps(M.from_map(model, vconv=M.to_str))
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        state_row = AppState(key="state", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/fr_3_2_REQ_10", response_model=dict)
def fr_3_2_REQ_10(request: dict) -> dict:
    db = next(get_db_session())
    try:
        model = load_model(db)
        event_id = request.get("eventId")
        event_data = request.get("eventData")
        if event_id is None or event_data is None:
            raise HTTPException(status_code=400, detail="Missing eventId or eventData")
        action = core.Action_AppendEvent(M.to_str(event_id), M.to_str(event_data))
        new_model = Dom.Normalize(Dom.Apply(model, action))
        save_model(db, new_model)
        return {"message": "Event appended successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))