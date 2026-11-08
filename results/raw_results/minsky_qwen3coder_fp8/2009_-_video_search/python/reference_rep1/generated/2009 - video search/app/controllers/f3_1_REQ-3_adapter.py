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
from sqlalchemy.orm import Session
from app.extensions import SessionLocal

from typing import Optional

router = APIRouter()

# Database model for storing the state
from sqlalchemy import Column, Integer, String, Text
from app.extensions import Base

from app.controllers.f3_1_REQ-1_adapter import AppState

# Helper to get the session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper to get or create the state
# This assumes a single state value for this feature
# If multiple features need state, consider a more complex keying scheme
STATE_KEY = "torrent_search_enabled"

def get_current_state(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == STATE_KEY).first()
    if state_row is None:
        return Dom.Init()
    else:
        # Deserialize the JSON value into a Python object
        state_dict = M.from_str(state_row.value)
        # Convert to Dafny model
        return M.from_bool(state_dict)

# Helper to persist the state
# Note: We're using a simple key-value store for the state
# In a real application, you might want to use a more robust approach
# such as a separate table for each feature or a JSONB column

def save_state(db: Session, new_state: Dom.Model):
    # Serialize the Dafny model to a JSON-serializable Python object
    state_json = M.to_bool(new_state)
    # Convert to JSON string
    state_str = M.to_str(state_json)
    
    # Get or create the state row
    state_row = db.query(AppState).filter(AppState.key == STATE_KEY).first()
    if state_row is None:
        state_row = AppState(key=STATE_KEY, value=state_str)
        db.add(state_row)
    else:
        state_row.value = state_str
    
    db.commit()

@router.post("/toggle-torrent-search")
async def toggle_torrent_search(include_torrents: bool):
    # This endpoint toggles the torrent search setting
    # It takes a boolean indicating whether torrents should be included
    
    # Get the database session
    db = next(get_db())
    
    # Get the current state
    current_state = get_current_state(db)
    
    # Create the action
    action = core.Action_ToggleTorrentSearch()
    
    # Apply the action to the state
    new_state = Dom.Normalize(Dom.Apply(current_state, action))
    
    # Save the new state
    save_state(db, new_state)
    
    # Return the new state as JSON
    return {"torrent_search_enabled": M.from_bool(new_state)}
