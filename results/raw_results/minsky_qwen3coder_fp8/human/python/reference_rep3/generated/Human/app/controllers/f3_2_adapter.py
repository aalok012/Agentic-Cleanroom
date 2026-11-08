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

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.human.python.reference_rep3.generated.Human.app.extensions import SessionLocal, Base, engine
from sqlalchemy import Column, Integer, String, Text
import json

class AppState(Base):
    __tablename__ = "app_state"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(Text)

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

def get_model(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "f3_2_state").first()
    if state_row is None:
        return Dom.Init()
    return M.from_seq(json.loads(state_row.value), lambda x: M.from_str(x))

def save_model(db: Session, model: Dom.Model):
    value = M.to_seq(model, lambda x: M.to_str(x))
    state_row = db.query(AppState).filter(AppState.key == "f3_2_state").first()
    if state_row is None:
        state_row = AppState(key="f3_2_state", value=json.dumps(value))
        db.add(state_row)
    else:
        state_row.value = json.dumps(value)
    db.commit()

@router.post("/register_for_event")
def register_for_event(request: Request, db: Session = Depends(get_db)):
    # Check if user is authenticated
    # This is a placeholder check - in real implementation, you'd check session/token
    if not hasattr(request.state, 'user_id') or request.state.user_id is None:
        raise HTTPException(status_code=401, detail="User not authenticated. Please log in.")
    
    # Get the event ID from the request
    event_id = request.query_params.get("event_id")
    if not event_id:
        raise HTTPException(status_code=400, detail="Event ID is required")
    
    # Load current state
    current_state = get_model(db)
    
    # Create action
    action = core.Action_RegisterForEvent(M.to_str(event_id))
    
    # Apply action
    new_state = Dom.Normalize(Dom.Apply(current_state, action))
    
    # Save new state
    save_model(db, new_state)
    
    # Return success response
    return {
        "message": "Successfully registered for event",
        "event_id": event_id,
        "registered_events": M.from_seq(new_state[1], lambda x: M.from_str(x))
    }