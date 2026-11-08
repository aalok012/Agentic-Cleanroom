import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_2_REQ_9-py"))
import dafny_marshal as M
import F3__2__REQ__9Domain as core
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

def load_model(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        return Dom.Init()
    return M.from_map(json.loads(state_row.value), vconv=bool)


def save_model(db: Session, model: Dom.Model) -> None:
    json_value = json.dumps(M.from_map(model, vconv=bool))
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        state_row = AppState(key="model", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/manage_client_access")
async def manage_client_access(action: str, client_id: str):
    if action not in ["AddClient", "RemoveClient"]:
        raise HTTPException(status_code=400, detail="Invalid action. Must be 'AddClient' or 'RemoveClient'.")
    
    with next(get_db_session()) as db:
        model = load_model(db)
        
        # Construct the action based on input
        if action == "AddClient":
            dafny_action = core.Action_AddClient(M.to_str(client_id))
        elif action == "RemoveClient":
            dafny_action = core.Action_RemoveClient(M.to_str(client_id))
        
        # Apply the action using the proved core
        new_model = Dom.Normalize(Dom.Apply(model, dafny_action))
        
        # Save the updated model
        save_model(db, new_model)
        
        return {"status": "success", "message": f"Client {client_id} {action.lower()[4:]}."}
