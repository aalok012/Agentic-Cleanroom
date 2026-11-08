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
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal, engine

import json

from app.controllers.f3_1_REQ-1_adapter import AppState

Base.metadata.create_all(engine)

router = APIRouter()

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_model(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        return Dom.Init()
    return M.from_seq(json.loads(state_row.value), lambda x: M.from_str(x))

def set_model(db: Session, model: Dom.Model) -> None:
    value = M.to_seq(model, M.to_str)
    state_row = db.query(AppState).filter(AppState.key == "state").first()
    if state_row is None:
        state_row = AppState(key="state", value=json.dumps(value))
        db.add(state_row)
    else:
        state_row.value = json.dumps(value)
    db.commit()

@router.post("/fr_3_1_REQ_5")
def fr_3_1_REQ_5(request: dict) -> dict:
    with next(get_db_session()) as db:
        model = get_model(db)
        query = request.get("query", "")
        action = core.Action_Search(M.to_str(query))
        new_model = Dom.Normalize(Dom.Apply(model, action))
        set_model(db, new_model)
        
        # Extract the message from the model
        message, _ = new_model
        return {"message": M.from_str(message)}