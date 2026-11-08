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

from app.controllers.f3_2_REQ-1_adapter import AppState

Base.metadata.create_all(engine)

router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_model(db: Session) -> Dom.Model:
    row = db.query(AppState).filter(AppState.key == "state").first()
    if row is None:
        return Dom.Init()
    return M.from_map(json.loads(row.value), vconv=str)

def save_model(db: Session, model: Dom.Model) -> None:
    json_value = json.dumps(M.from_map(model, vconv=str))
    row = db.query(AppState).filter(AppState.key == "state").first()
    if row is None:
        db.add(AppState(key="state", value=json_value))
    else:
        row.value = json_value
    db.commit()

@router.post("/events")
def append_event(event_data: dict[str, str]):
    with next(get_db_session()) as db:
        model = load_model(db)
        # Convert event_data to Dafny Action
        # Since event_data is a dict, we need to extract the eventId and eventData
        # Assuming event_data has exactly one key-value pair
        if len(event_data) != 1:
            raise HTTPException(status_code=400, detail="event_data must contain exactly one key-value pair")
        
        event_id = list(event_data.keys())[0]
        event_data_value = list(event_data.values())[0]
        
        action = core.Action_AppendEvent(M.to_str(event_id), M.to_str(event_data_value))
        new_model = Dom.Normalize(Dom.Apply(model, action))
        save_model(db, new_model)
        return {"status": "success"}