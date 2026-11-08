import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_1_REQ_1-py"))
import dafny_marshal as M
import F3__1__REQ__1Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine

# Define the state table
Base = declarative_base()

class AppState(Base):
    __tablename__ = "app_state"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(Text)

# Create tables
Base.metadata.create_all(engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_state(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        return Dom.Init()
    return M.from_map(state_row.value, vconv=str)

def save_state(db: Session, model: Dom.Model):
    json_value = M.to_map(model, vconv=M.to_str)
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        state_row = AppState(key="model", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/fr_3_1_REQ_1", response_model=dict)
def fr_3_1_REQ_1(request: dict):
    db = next(get_db())
    try:
        # Load the current state
        state = load_state(db)
        
        # Extract query from request
        query = request.get("query", "")
        
        # Create the action
        action = core.Action_Search(M.to_str(query))
        
        # Apply the action to the state
        new_state = Dom.Normalize(Dom.Apply(state, action))
        
        # Save the new state
        save_state(db, new_state)
        
        # Return the response
        return {"message": "Torrent search will share the same search bar with the streaming search."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))