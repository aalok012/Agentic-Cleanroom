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

from app.controllers.f3_2_REQ-10_adapter import AppState

Base.metadata.create_all(engine)

router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_model(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        return Dom.Init()
    return M.from_seq(json.loads(state_row.value), lambda x: (M.from_str(x[0]), x[1]))

def save_model(db: Session, model: Dom.Model):
    value = M.to_seq(model, lambda x: (M.to_str(x[0]), x[1]))
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        state_row = AppState(key="model", value=json.dumps(value))
        db.add(state_row)
    else:
        state_row.value = json.dumps(value)
    db.commit()

@router.post("/check_admin_access")
async def check_admin_access(user_credentials: dict[str, str], db: Session = Depends(get_db_session)):
    # Precondition: The user has valid administrative credentials and permissions
    if "adminId" not in user_credentials or "clientId" not in user_credentials:
        raise HTTPException(status_code=400, detail="Missing adminId or clientId in credentials")
    
    # Load current state
    model = load_model(db)
    
    # Construct action
    action = core.Action_AccessClientData(
        M.to_str(user_credentials["adminId"]),
        M.to_str(user_credentials["clientId"])
    )
    
    # Apply action to model
    new_model = Dom.Normalize(Dom.Apply(model, action))
    
    # Save updated model
    save_model(db, new_model)
    
    # Return result
    return {"access_granted": new_model[1]}
