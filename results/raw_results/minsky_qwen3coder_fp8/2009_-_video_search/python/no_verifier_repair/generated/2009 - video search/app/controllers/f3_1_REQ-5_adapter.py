import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_1_REQ_5-py"))
import dafny_marshal as M
import F3__1__REQ__5Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.extensions import SessionLocal

from typing import List, Dict, Any

router = APIRouter()

class AppState:
    __tablename__ = "app_state"
    id = None  # Will be set by SQLAlchemy
    key = "search_state"
    value = ""

    def __init__(self, key="search_state", value=""):
        self.key = key
        self.value = value

    @staticmethod
    def get_state(db: Session):
        state_row = db.query(AppState).filter(AppState.key == "search_state").first()
        if state_row is None:
            return Dom.Init()
        else:
            return M.from_str(state_row.value)

    @staticmethod
    def save_state(db: Session, model):
        json_value = M.to_str(model)
        state_row = db.query(AppState).filter(AppState.key == "search_state").first()
        if state_row is None:
            new_row = AppState(key="search_state", value=json_value)
            db.add(new_row)
        else:
            state_row.value = json_value
        db.commit()

@router.post("/search")
def handle_search_results(results: List[Dict[str, Any]]) -> str:
    db = SessionLocal()
    try:
        # Load the current state
        model = AppState.get_state(db)
        
        # Check if results are empty
        if len(results) > 0:
            # In this implementation, we assume that if results are provided,
            # we don't perform any action since the requirement is specifically
            # about handling no results.
            # However, for completeness, we could apply an action here if needed.
            pass
        else:
            # Create the action for no results
            action = core.Action_SearchNoResults()
            
            # Apply the action to the model
            new_model = Dom.Normalize(Dom.Apply(model, action))
            
            # Save the new state
            AppState.save_state(db, new_model)
            
            # Return the message
            return M.from_str(new_model)
        
        # If there are results, return empty string or handle accordingly
        return ""
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()