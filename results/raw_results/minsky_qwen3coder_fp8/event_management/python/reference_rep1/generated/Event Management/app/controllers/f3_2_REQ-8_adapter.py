import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_2_REQ_8-py"))
import dafny_marshal as M
import F3__2__REQ__8Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine
import json

# Define the state table
Base = declarative_base()

from app.controllers.f3_2_REQ-10_adapter import AppState

# Create tables
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
    return M.from_seq(json.loads(state_row.value), lambda x: M.from_str(x))

def save_state(db: Session, model: Dom.Model) -> None:
    json_value = json.dumps(M.to_seq(model, M.to_str))
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        new_row = AppState(key="state", value=json_value)
        db.add(new_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/check_admin_access", response_model=bool)
def check_admin_access(user_credentials: dict[str, str]):
    with next(get_db_session()) as db:
        # Load current state
        state = load_state(db)
        
        # Validate input
        if "adminId" not in user_credentials or "clientId" not in user_credentials:
            raise HTTPException(status_code=400, detail="Missing required fields: adminId or clientId")
        
        # Construct action
        action = core.Action_AccessClientData(
            M.to_str(user_credentials["adminId"]),
            M.to_str(user_credentials["clientId"])
        )
        
        # Apply action to state
        new_state = Dom.Normalize(Dom.Apply(state, action))
        
        # Save updated state
        save_state(db, new_state)
        
        # Extract result
        _, has_access, _ = new_state
        return has_access