import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_1_REQ_3-py"))
import dafny_marshal as M
import F3__1__REQ__3Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine
import json

# Create the table
Base.metadata.create_all(engine)

from app.controllers.f3_1_REQ-1_adapter import AppState

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fr_3_1_REQ_3(request: dict) -> dict:
    # Get the database session
    db = next(get_db())
    
    # Load the current state or initialize to default
    state_row = db.query(AppState).filter(AppState.key == "fr_3_1_REQ_3_state").first()
    if state_row:
        model = M.from_str(state_row.value)
    else:
        model = Dom.Init()
    
    # Build the action from the request
    action = core.Action_IncludeSearch()
    
    # Apply the action to the model
    new_state = Dom.Normalize(Dom.Apply(model, action))
    
    # Marshal the new state to JSON
    new_state_json = M.to_str(new_state)
    
    # Save the new state back to the database
    if state_row:
        state_row.value = new_state_json
    else:
        state_row = AppState(key="fr_3_1_REQ_3_state", value=new_state_json)
        db.add(state_row)
    
    db.commit()
    
    # Return the response
    return {"message": "Torrent search inclusion updated successfully"}