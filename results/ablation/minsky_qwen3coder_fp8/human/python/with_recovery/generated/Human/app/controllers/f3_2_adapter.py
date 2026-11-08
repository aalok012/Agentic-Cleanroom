import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_2-py"))
import dafny_marshal as M
import F3__2Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.human.python.with_recovery.generated.Human.app.extensions import Base, SessionLocal, engine

Base.metadata.create_all(engine)

from results.ablation.minsky_qwen3coder_fp8.human.python.with_recovery.generated.Human.app.controllers.f3_1_adapter import AppState

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_model(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "F3_2").first()
    if state_row is None:
        return Dom.Init()
    return M.from_json(state_row.value, Dom.Model)

def set_model(db: Session, model: Dom.Model):
    json_value = M.to_json(model)
    state_row = db.query(AppState).filter(AppState.key == "F3_2").first()
    if state_row is None:
        state_row = AppState(key="F3_2", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/prompt_user_to_log_in")
def prompt_user_to_log_in(request: Request, db: Session = next(get_db())):
    # Check if user is authenticated
    # This is a placeholder check - in real implementation, you'd check session or token
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        # Simulate unauthenticated user
        raise HTTPException(status_code=401, detail="User is not authenticated. Please log in.")
    
    # Get current model
    model = get_model(db)
    
    # Create action
    action = core.Action_RegisterForEvent(M.to_str("event_id_placeholder"))
    
    # Apply action
    new_model = Dom.Normalize(Dom.Apply(model, action))
    
    # Save updated model
    set_model(db, new_model)
    
    # Return success response
    return {"message": "User is registered for the event"}
