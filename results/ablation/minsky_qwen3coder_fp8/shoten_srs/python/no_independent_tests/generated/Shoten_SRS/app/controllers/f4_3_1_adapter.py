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

from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.extensions import Base, SessionLocal, engine

Base.metadata.create_all(engine)

# State persistence model

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.controllers.f4_11_adapter import AppState

router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_model(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        return Dom.Init()
    return M.from_json(state_row.value, Dom.Model)

def save_model(db: Session, model: Dom.Model) -> None:
    json_value = M.to_json(model)
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        state_row = AppState(key="model", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()

@router.get("/search-interface")
def display_search_interface():
    # This endpoint simulates the UI display of the search interface.
    # In a real application, this would return HTML or a frontend component.
    return {"message": "Displaying search interface"}

@router.post("/search-books")
def search_books(query: str):
    # This endpoint handles the search query and returns matching books.
    # It uses the Dafny core to manage state transitions.
    
    with next(get_db_session()) as db:
        model = load_model(db)
        
        # Apply the SearchBook action
        action = core.Action_SearchBook()
        new_model = Dom.Normalize(Dom.Apply(model, action))
        
        # Save the updated model
        save_model(db, new_model)
        
        # For demonstration purposes, we'll return a mock list of books
        # In a real implementation, this would involve querying a database or external API
        return [
            {
                "title": "Dafny Programming Guide",
                "author": "John Doe",
                "isbn": "978-0123456789",
                "price": 29.99,
                "availability": True,
                "condition": "New",
                "coverImage": "https://example.com/dafny-guide.jpg"
            },
            {
                "title": "FastAPI Best Practices",
                "author": "Jane Smith",
                "isbn": "978-0987654321",
                "price": 39.99,
                "availability": False,
                "condition": "Used",
                "coverImage": "https://example.com/fastapi-best-practices.jpg"
            }
        ]