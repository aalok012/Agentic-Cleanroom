import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_1_REQ_6-py"))
import dafny_marshal as M
import F3__1__REQ__6Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine

Base.metadata.create_all(engine)

from app.controllers.f3_1_REQ-1_adapter import AppState

router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_model(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "torrent_sort_state").first()
    if state_row is None:
        return Dom.Init()
    return M.from_str(state_row.value, Dom.Model)

def save_model(db: Session, model: Dom.Model) -> None:
    json_value = M.to_str(model)
    state_row = db.query(AppState).filter(AppState.key == "torrent_sort_state").first()
    if state_row is None:
        state_row = AppState(key="torrent_sort_state", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/sort-torrent-results")
def sort_torrent_results(results: list[dict[str, str]], sort_by: str):
    with next(get_db_session()) as db:
        model = load_model(db)
        
        # Validate sort_by
        if sort_by not in ["size", "date", "alpha"]:
            raise HTTPException(status_code=400, detail="Invalid sort_by value. Must be 'size', 'date', or 'alpha'.")
        
        # Create action based on sort_by
        if sort_by == "size":
            action = core.Action_SortBySize()
        elif sort_by == "date":
            action = core.Action_SortByDate()
        else:  # alpha
            action = core.Action_SortByAlpha()
        
        # Apply the action to the model
        new_model = Dom.Normalize(Dom.Apply(model, action))
        
        # Save the updated model
        save_model(db, new_model)
        
        # Return the sorted results
        return {"results": results}
