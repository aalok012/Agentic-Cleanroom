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
    return M.from_map(json.loads(state_row.value), vconv=bool)


def save_model(db: Session, model: Dom.Model):
    json_value = json.dumps(M.from_map(model, vconv=bool))
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        state_row = AppState(key="model", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()


def fr_3_2_REQ_9(request: dict) -> dict:
    with next(get_db_session()) as db:
        model = load_model(db)
        
        action = None
        if "add_client" in request:
            action = core.Action_AddClient(M.to_str(request["add_client"]))
        elif "delete_client" in request:
            action = core.Action_DeleteClient(M.to_str(request["delete_client"]))
        else:
            raise HTTPException(status_code=400, detail="Invalid action: must specify 'add_client' or 'delete_client'")
        
        new_model = Dom.Normalize(Dom.Apply(model, action))
        save_model(db, new_model)
        
        return {"status": "success", "clients": list(M.from_map(new_model, vconv=bool).keys())}
