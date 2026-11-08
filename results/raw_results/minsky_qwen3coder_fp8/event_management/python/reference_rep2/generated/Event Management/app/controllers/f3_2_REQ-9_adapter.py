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

Base.metadata.create_all(engine)

from app.controllers.f3_2_REQ-1_adapter import AppState

router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_model(db: Session) -> Dom.Model:
    row = db.query(AppState).filter(AppState.key == "model").first()
    if row is None:
        return Dom.Init()
    return M.from_map(json.loads(row.value), vconv=lambda x: M.from_seq(x, M.from_str))

def save_model(db: Session, model: Dom.Model) -> None:
    json_value = json.dumps(M.to_map(model, vconv=lambda s: M.to_seq(s, M.to_str)))
    row = db.query(AppState).filter(AppState.key == "model").first()
    if row is None:
        row = AppState(key="model", value=json_value)
        db.add(row)
    else:
        row.value = json_value
    db.commit()

@router.post("/client-access")
def manage_client_access(client_id: str, permissions: list[str], action: str) -> dict[str, str]:
    with next(get_db_session()) as db:
        model = get_model(db)
        
        if action == "add":
            action_obj = core.Action_AddClientAccess(M.to_str(client_id), M.to_set(permissions, M.to_str))
        elif action == "delete":
            # For deletion, we need to remove permissions from existing client
            if client_id not in model:
                raise HTTPException(status_code=404, detail="Client not found")
            # Create a new set without the specified permissions
            old_permissions = model[client_id]
            new_permissions = old_permissions - M.to_set(permissions, M.to_str)
            action_obj = core.Action_AddClientAccess(M.to_str(client_id), new_permissions)
        else:
            raise HTTPException(status_code=400, detail="Invalid action. Must be 'add' or 'delete'")
        
        new_state = Dom.Normalize(Dom.Apply(model, action_obj))
        save_model(db, new_state)
        
        return {"status": "success", "message": f"Client access {action}ed successfully"}
