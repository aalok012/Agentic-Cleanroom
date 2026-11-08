import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_2_REQ_7-py"))
import dafny_marshal as M
import F3__2__REQ__7Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine

Base.metadata.create_all(engine)

router = APIRouter()

from app.controllers.f3_2_REQ-10_adapter import AppState


def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def fr_3_2_REQ_7(request: dict) -> dict:
    db = next(get_db_session())
    
    # Load existing state or initialize to empty
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row:
        state = M.from_map(state_row.value, vconv=str)
    else:
        state = Dom.Init()
    
    # Convert request to Dafny action
    action_type = request.get("action")
    if action_type == "Add":
        action = core.Action_Add(M.to_str(request["key"]), M.to_str(request["value"]))
    elif action_type == "Update":
        action = core.Action_Update(M.to_str(request["key"]), M.to_str(request["value"]))
    elif action_type == "Delete":
        action = core.Action_Delete(M.to_str(request["key"]))
    elif action_type == "Retrieve":
        action = core.Action_Retrieve(M.to_str(request["key"]))
    else:
        raise HTTPException(status_code=400, detail="Invalid action type")
    
    # Apply action to state
    new_state = Dom.Normalize(Dom.Apply(state, action))
    
    # Serialize new state and save it
    json_state = M.to_map(new_state)
    serialized_state = json.dumps(json_state)
    
    if state_row:
        state_row.value = serialized_state
    else:
        state_row = AppState(key="state", value=serialized_state)
        db.add(state_row)
    
    db.commit()
    
    # Return appropriate response based on action
    if action_type == "Retrieve":
        return {"result": M.from_str(new_state[request["key"]])}
    else:
        return {"status": "success"}