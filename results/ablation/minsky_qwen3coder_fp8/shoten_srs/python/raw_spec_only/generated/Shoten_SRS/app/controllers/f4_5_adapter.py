import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F4_5-py"))
import dafny_marshal as M
import F4__5Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal, engine

Base.metadata.create_all(engine)

router = APIRouter()

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.f4_10_adapter import AppState


def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_model(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "cart").first()
    if state_row is None:
        return Dom.Init()
    return M.from_map(state_row.value, vconv=int)


def save_model(db: Session, model: Dom.Model):
    json_value = M.to_map(M.from_map(model, vconv=int))
    state_row = db.query(AppState).filter(AppState.key == "cart").first()
    if state_row is None:
        state_row = AppState(key="cart", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()


def fr_4_5_REQ_1(request: dict) -> dict:
    # This route is a no-op since the action is handled by REQ-2 and REQ-3
    return {"message": "Book removal initiated"}


def fr_4_5_REQ_2(request: dict) -> dict:
    # Validate that the user is authenticated
    if "user_id" not in request or not request["user_id"]:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    # Validate that the book exists in the cart
    with next(get_db_session()) as db:
        model = get_model(db)
        book = request.get("book")
        if book is None:
            raise HTTPException(status_code=400, detail="Book name required")
        
        if book not in model:
            raise HTTPException(status_code=404, detail="Book not found in cart")
    
    return {"message": "Book selected for removal"}


def fr_4_5_REQ_3(request: dict) -> dict:
    # Validate that the user is authenticated
    if "user_id" not in request or not request["user_id"]:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    # Validate that the book exists in the cart
    with next(get_db_session()) as db:
        model = get_model(db)
        book = request.get("book")
        if book is None:
            raise HTTPException(status_code=400, detail="Book name required")
        
        if book not in model:
            raise HTTPException(status_code=404, detail="Book not found in cart")
        
        # Create the action
        action = core.Action_Remove(M.to_str(book))
        
        # Apply the action
        new_model = Dom.Normalize(Dom.Apply(model, action))
        
        # Save the new model
        save_model(db, new_model)
        
        # Return the updated cart
        return {"cart": M.from_map(new_model, vconv=int)}