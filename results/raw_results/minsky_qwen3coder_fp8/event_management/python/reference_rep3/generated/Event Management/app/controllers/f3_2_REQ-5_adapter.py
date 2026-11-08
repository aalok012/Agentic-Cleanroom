import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_2_REQ_5-py"))
import dafny_marshal as M
import F3__2__REQ__5Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine

Base.metadata.create_all(engine)

router = APIRouter()

from app.controllers.f3_2_REQ-1_adapter import AppState


def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_registrant_list() -> list[dict[str, str]]:
    db = next(get_db_session())
    
    # Load the current state from the database
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    
    # If no state exists, start with the initial state
    if state_row is None:
        model = Dom.Init()
    else:
        # Deserialize the stored state
        stored_state = state_row.value
        model = M.from_map(stored_state, vconv=str)
    
    # Create the action
    action = core.Action_GenerateRegistrantList()
    
    # Apply the action to the model (this is the PROVED transition)
    new_model = Dom.Normalize(Dom.Apply(model, action))
    
    # Serialize the new state back to JSON
    serialized_state = M.to_map(new_model)
    
    # Update the database with the new state
    if state_row is None:
        new_row = AppState(key="state", value=serialized_state)
        db.add(new_row)
    else:
        state_row.value = serialized_state
    
    db.commit()
    
    # Return the list of registrants
    return M.from_map(new_model, vconv=str)