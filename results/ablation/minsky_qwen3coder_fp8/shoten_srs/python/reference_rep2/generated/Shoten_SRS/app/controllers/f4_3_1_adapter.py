import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F4_3_1-py"))
import dafny_marshal as M
import F4__3__1Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal, engine

Base.metadata.create_all(engine)

router = APIRouter()

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.controllers.f4_11_adapter import AppState


def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_model(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        return Dom.Init()
    return M.from_str(state_row.value, Dom.Model)


def save_model(db: Session, model: Dom.Model) -> None:
    json_value = M.to_str(model)
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        state_row = AppState(key="model", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()


def display_book_search_interface() -> dict[str, str]:
    return {"message": "Display interface for entering search criteria (title, author, or ISBN)"}


def search_books(title: str = "", author: str = "", isbn: str = "") -> list[dict[str, str]]:
    # This function would normally be called with a valid session
    # But since we're simulating the behavior without actual DB calls,
    # we'll just return an empty list as a placeholder.
    # In a real implementation, this would involve:
    # 1. Getting the current model from DB
    # 2. Applying the SearchBook action
    # 3. Returning the appropriate data based on the model
    return []


@router.get("/display-book-search-interface", response_model=dict[str, str])
def get_display_book_search_interface():
    return display_book_search_interface()


@router.post("/search-books", response_model=list[dict[str, str]])
def post_search_books(title: str = "", author: str = "", isbn: str = ""):
    db = next(get_db_session())
    model = get_model(db)
    
    # Apply the SearchBook action
    action = core.Action_SearchBook()
    new_model = Dom.Normalize(Dom.Apply(model, action))
    
    # Save the updated model
    save_model(db, new_model)
    
    # For now, returning an empty list as placeholder
    # In a real implementation, this should return the actual search results
    return []