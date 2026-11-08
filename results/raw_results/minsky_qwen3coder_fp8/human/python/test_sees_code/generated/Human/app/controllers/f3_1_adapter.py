import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_1-py"))
import dafny_marshal as M
import F3__1Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.human.python.test_sees_code.generated.Human.app.extensions import Base, SessionLocal, engine

Base.metadata.create_all(engine)

class AppState(Base):
    __tablename__ = "app_state"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(Text)

router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_state(db: Session, key: str) -> Dom.Model:
    row = db.query(AppState).filter(AppState.key == key).first()
    if row is None:
        return Dom.Init()
    return M.from_seq(M.from_str(row.value), lambda x: M.from_map(x, vconv=int))

def save_state(db: Session, key: str, state: Dom.Model) -> None:
    json_value = M.to_str(M.to_seq(state, lambda x: M.to_map(x, vconv=str)))
    row = db.query(AppState).filter(AppState.key == key).first()
    if row is None:
        db.add(AppState(key=key, value=json_value))
    else:
        row.value = json_value
    db.commit()

@router.put("/events/{event_id}/details")
def edit_event_details_and_registration(event_id: str, details: dict, registration_requirements: dict):
    with next(get_db_session()) as db:
        state = load_state(db, event_id)
        action = core.Action_EditEventDetails(
            M.to_map(details),
            M.to_map(registration_requirements)
        )
        new_state = Dom.Normalize(Dom.Apply(state, action))
        save_state(db, event_id, new_state)
        return {
            "event_id": event_id,
            "details": M.from_map(new_state[1], vconv=str),
            "registration_requirements": M.from_map(new_state[2], vconv=str)
        }