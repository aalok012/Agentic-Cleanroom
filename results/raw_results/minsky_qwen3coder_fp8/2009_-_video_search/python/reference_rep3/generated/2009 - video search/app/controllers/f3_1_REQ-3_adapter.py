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

class AppState:
    __tablename__ = "app_state"
    id: int
    key: str
    value: str

# Helper to get or create the state
def get_or_create_state(db: Session, key: str):
    state = db.query(AppState).filter(AppState.key == key).first()
    if not state:
        # Initialize with the initial state
        initial_model = Dom.Init()
        state = AppState(key=key, value=M.from_str(M.to_str(initial_model)))
        db.add(state)
        db.commit()
        db.refresh(state)
    return state

# Helper to update the state
def update_state(db: Session, key: str, new_model):
    state = get_or_create_state(db, key)
    state.value = M.from_str(M.to_str(new_model))
    db.commit()
    db.refresh(state)
    return state

@router.post("/configure_torrent_search")
def configure_torrent_search(include_torrents: bool):
    db = SessionLocal()
    try:
        # Load the current model
        state_row = get_or_create_state(db, "torrent_search_config")
        model = M.to_str(state_row.value)
        model = M.from_str(model)
        
        # Create the action
        action = core.Action_ToggleSearch()
        
        # Apply the action to the model
        new_model = Dom.Normalize(Dom.Apply(model, action))
        
        # Update the state
        update_state(db, "torrent_search_config", new_model)
        
        # Return the updated configuration
        return {"include_torrents": new_model}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()