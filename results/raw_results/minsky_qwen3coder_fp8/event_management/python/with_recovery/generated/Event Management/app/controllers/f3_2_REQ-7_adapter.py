from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.extensions import SessionLocal
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

from typing import Dict, Any
from pydantic import BaseModel

# Database model
from sqlalchemy import Column, Integer, String, Text
from app.extensions import Base

from app.controllers.f3_2_REQ-10_adapter import AppState

# Pydantic models

class WorkflowStepRequest(BaseModel):
    step_type: str
    data: Dict[str, Any]

class WorkflowStepResponse(BaseModel):
    next_step: str
    state: Dict[str, str]

# Router
router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_state(db: Session) -> core.Model:
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        return Dom.Init()
    else:
        return M.from_map(state_row.value, vconv=str)

def save_state(db: Session, state: core.Model) -> None:
    json_state = M.to_map(state)
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        state_row = AppState(key="state", value=json_state)
        db.add(state_row)
    else:
        state_row.value = json_state
    db.commit()

@router.post("/workflow-step", response_model=WorkflowStepResponse)
def execute_workflow_step(request: WorkflowStepRequest):
    db = next(get_db_session())
    
    # Get current state
    current_state = get_current_state(db)
    
    # Determine action based on step_type
    action = None
    if request.step_type == "DataEntry":
        action = core.Action_DataEntry()
    elif request.step_type == "DataOrganization":
        action = core.Action_DataOrganization()
    elif request.step_type == "DataRetrieval":
        action = core.Action_DataRetrieval()
    elif request.step_type == "DataModification":
        action = core.Action_DataModification()
    elif request.step_type == "DataDeletion":
        action = core.Action_DataDeletion()
    else:
        raise HTTPException(status_code=400, detail="Invalid step type")
    
    # Apply the action to the state
    new_state = Dom.Normalize(Dom.Apply(current_state, action))
    
    # Save the new state
    save_state(db, new_state)
    
    # Prepare response
    response_data = {
        "next_step": "Continue with next step",
        "state": M.from_map(new_state, vconv=str)
    }
    
    return response_data