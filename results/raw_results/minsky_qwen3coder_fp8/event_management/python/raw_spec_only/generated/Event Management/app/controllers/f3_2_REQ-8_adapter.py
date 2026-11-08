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

def fr_3_2_REQ_8(request: dict) -> dict:
    db = next(get_db_session())
    
    # Load existing state or initialize to empty
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row:
        model = M.from_map(json.loads(state_row.value), vconv=bool)
    else:
        model = Dom.Init()
    
    # Validate request
    if "clientId" not in request:
        raise HTTPException(status_code=400, detail="Missing clientId in request")
    
    # Construct action
    client_id = M.to_str(request["clientId"])
    action = core.Action_GrantAccess(client_id)
    
    # Apply action to state
    new_model = Dom.Normalize(Dom.Apply(model, action))
    
    # Serialize new state
    new_state_json = json.dumps(M.from_map(new_model, vconv=bool))
    
    # Save new state
    if state_row:
        state_row.value = new_state_json
    else:
        state_row = AppState(key="state", value=new_state_json)
        db.add(state_row)
    
    db.commit()
    
    return {"message": "Provide administrative access to the clients."}