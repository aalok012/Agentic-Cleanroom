import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F4_14-py"))
import dafny_marshal as M
import F4__14Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal, engine

# Ensure the table exists
Base.metadata.create_all(engine)

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.f4_10_adapter import AppState

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
    return M.from_seq(M.from_str(state_row.value), lambda x: x)

def save_state(db: Session, state: Dom.Model) -> None:
    json_value = M.to_str(M.to_seq(state, lambda x: x))
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        new_row = AppState(key="state", value=json_value)
        db.add(new_row)
    else:
        state_row.value = json_value
    db.commit()

# FR 4.14.REQ-1: The system shall allow the registered and logged-in user to exit his/her account, so that access to operations requiring a user to be logged in are now disabled.
def fr_4_14_REQ_1(request: dict) -> dict:
    with next(get_db_session()) as db:
        # Precondition check: User must be logged in
        current_state = load_state(db)
        if not current_state[0]:  # loggedIn is False
            raise HTTPException(status_code=400, detail="User is not logged in")
        
        # Build the action
        action = core.Action_Logout()
        
        # Apply the action
        new_state = Dom.Normalize(Dom.Apply(current_state, action))
        
        # Save the new state
        save_state(db, new_state)
        
        # Return the response
        return {"message": "User logged out successfully", "logged_in": new_state[0], "username": new_state[1]}
