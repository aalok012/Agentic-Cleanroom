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

Base.metadata.create_all(engine)

from app.controllers.f3_2_REQ-10_adapter import AppState

router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_state(db: Session) -> Dom.Model:
    row = db.query(AppState).filter(AppState.key == "state").first()
    if row is None:
        return Dom.Init()
    return M.from_map(row.value, vconv=bool)

def save_state(db: Session, state: Dom.Model) -> None:
    json_value = M.to_map(state, vconv=lambda x: str(x).lower())
    row = db.query(AppState).filter(AppState.key == "state").first()
    if row is None:
        row = AppState(key="state", value=json_value)
        db.add(row)
    else:
        row.value = json_value
    db.commit()

@router.post("/manage_client_access")
async def manage_client_access(action: str, client_id: str):
    if action not in ["AddClient", "RemoveClient"]:
        raise HTTPException(status_code=400, detail="Invalid action. Must be 'AddClient' or 'RemoveClient'.")
    
    with next(get_db_session()) as db:
        model = load_state(db)
        
        if action == "AddClient":
            dafny_action = core.Action_AddClient(M.to_str(client_id))
        elif action == "RemoveClient":
            dafny_action = core.Action_RemoveClient(M.to_str(client_id))
        
        new_model = Dom.Normalize(Dom.Apply(model, dafny_action))
        save_state(db, new_model)
        
        return {"status": "success", "message": f"Client {client_id} {action.lower()[0:-6]}ed successfully."}
