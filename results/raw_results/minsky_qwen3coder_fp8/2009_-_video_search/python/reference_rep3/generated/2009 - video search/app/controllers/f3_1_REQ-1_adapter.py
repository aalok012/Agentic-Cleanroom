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

Base.metadata.create_all(engine)

router = APIRouter()

class AppState(Base):
    __tablename__ = "app_state"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(Text)


def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def search_torrents_and_streaming(query: str) -> dict[str, list[dict[str, str]]]:
    # Load the current state from the database
    db = next(get_db_session())
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    
    # Initialize the state if it doesn't exist
    if state_row is None:
        state = Dom.Init()
    else:
        # Deserialize the stored state
        state_json = state_row.value
        state = M.from_str(state_json, lambda x: M.from_seq(x, lambda y: M.from_str(y)))
    
    # Create the action
    action = core.Action_Search(M.to_str(query))
    
    # Apply the action to the state
    new_state = Dom.Normalize(Dom.Apply(state, action))
    
    # Serialize the new state
    new_state_json = M.to_str(new_state)
    
    # Save the new state back to the database
    if state_row is None:
        state_row = AppState(key="state", value=new_state_json)
        db.add(state_row)
    else:
        state_row.value = new_state_json
    
    db.commit()
    
    # Return the result
    # In this case, we're returning the query string since that's what was searched
    # and the torrents and streams sets are empty (as per the Dafny model)
    return {
        "query": query,
        "torrents": [],
        "streams": []
    }

@router.post("/search")
def search_endpoint(query: str):
    try:
        return search_torrents_and_streaming(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))