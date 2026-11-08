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

Base = declarative_base()

from app.controllers.f3_2_REQ-1_adapter import AppState

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
    return M.from_tuple(M.from_seq(json.loads(state_row.value), M.from_str), M.from_map)

def save_state(db: Session, state: Dom.Model) -> None:
    value = json.dumps(M.to_seq(M.to_tuple(state, M.to_str, M.to_map), M.to_str))
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        db.add(AppState(key="state", value=value))
    else:
        state_row.value = value
    db.commit()

@router.post("/manage_admin_client_access")
def manage_admin_client_access(admin_user_id: str, action: str, client_data: dict) -> dict:
    with next(get_db_session()) as db:
        model = load_state(db)
        
        # Build the action based on the input
        if action == "AccessClientData":
            dafny_action = core.Action_AccessClientData()
        elif action == "ModifyClientData":
            dafny_action = core.Action_ModifyClientData()
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
        
        # Apply the action to the model
        new_model = Dom.Normalize(Dom.Apply(model, dafny_action))
        
        # Save the new state
        save_state(db, new_model)
        
        # Return the result
        return {
            "access_granted": new_model[0],
            "client_data": M.from_map(new_model[1], vconv=M.from_str)
        }