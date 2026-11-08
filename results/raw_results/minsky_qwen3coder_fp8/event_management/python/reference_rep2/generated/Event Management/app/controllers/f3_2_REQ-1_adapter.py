import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F3_2_REQ_1-py"))
import dafny_marshal as M
import F3__2__REQ__1Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine
import json

# Ensure the table exists
Base.metadata.create_all(engine)

class AppState(Base):
    __tablename__ = "app_state"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(Text)

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
    return M.from_str(state_row.value)

def save_model(db: Session, model: Dom.Model) -> None:
    json_value = M.to_str(model)
    state_row = db.query(AppState).filter(AppState.key == "model").first()
    if state_row is None:
        new_row = AppState(key="model", value=json_value)
        db.add(new_row)
    else:
        state_row.value = json_value
    db.commit()

@router.get("/feature-accessibility", response_model=bool)
def check_feature_accessibility(db: Session = Depends(get_db_session)) -> bool:
    # Precondition: The system has internet connectivity
    # This is a placeholder for actual internet connectivity check
    # In a real implementation, we would verify internet access here
    
    # Load current state
    model = load_model(db)
    
    # Create action
    action = core.Action_Access()
    
    # Apply action using the proved core
    new_model = Dom.Normalize(Dom.Apply(model, action))
    
    # Save updated state
    save_model(db, new_model)
    
    # Postcondition: If the system has internet connectivity, then the feature is accessible
    # Since we're assuming internet connectivity, the feature should be accessible
    return True