from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import SessionLocal, Base, engine
from sqlalchemy import Column, Integer, String, Text
import json

# Ensure the table exists
Base.metadata.create_all(bind=engine)

class AppState(Base):
    __tablename__ = "app_state"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(Text)

router = APIRouter()

# Import the Dafny core
import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F4_11-py"))
import dafny_marshal as M
import F4__11Domain as core
Dom = core.default__


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_state(db: Session, user_id: str):
    state_row = db.query(AppState).filter(AppState.key == user_id).first()
    if state_row is None:
        return Dom.Init()
    return M.from_seq(json.loads(state_row.value), lambda x: M.from_str(x))


def save_user_state(db: Session, user_id: str, state):
    json_value = json.dumps(M.to_seq(state, lambda x: M.to_str(x)))
    state_row = db.query(AppState).filter(AppState.key == user_id).first()
    if state_row is None:
        new_row = AppState(key=user_id, value=json_value)
        db.add(new_row)
    else:
        state_row.value = json_value
    db.commit()


def initiate_account_update(user_id: str, update_data: dict) -> dict:
    # This endpoint simply acknowledges the initiation of an update.
    # The actual update happens via update_user_details.
    return {"message": "Account update initiated"}


def update_user_details(user_id: str, name: str, mailing_address: str, billing_address: str, payment_info: dict) -> dict:
    db = next(get_db())
    state = get_user_state(db, user_id)
    
    action = core.Action_UpdateAccountInfo(
        M.to_str(name),
        M.to_str(mailing_address),
        M.to_str(billing_address),
        M.to_str(str(payment_info))  # Convert dict to string for Dafny
    )
    
    new_state = Dom.Normalize(Dom.Apply(state, action))
    save_user_state(db, user_id, new_state)
    
    # Return the updated state
    return {
        "name": M.from_str(new_state[0]),
        "mailing_address": M.from_str(new_state[1]),
        "billing_address": M.from_str(new_state[2]),
        "payment_info": json.loads(M.from_str(new_state[3]))  # Convert back to dict
    }


def change_password(user_id: str, old_password: str, new_password: str, confirm_new_password: str) -> dict:
    db = next(get_db())
    state = get_user_state(db, user_id)
    
    # Validate that new passwords match
    if new_password != confirm_new_password:
        raise HTTPException(status_code=400, detail="New passwords do not match")
    
    action = core.Action_ChangePassword(
        M.to_str(old_password),
        M.to_str(new_password),
        M.to_str(confirm_new_password)
    )
    
    new_state = Dom.Normalize(Dom.Apply(state, action))
    
    # Check if password was actually changed (i.e., old password matched)
    if new_state == state:
        raise HTTPException(status_code=400, detail="Old password incorrect")
    
    save_user_state(db, user_id, new_state)
    
    return {"message": "Password changed successfully"}
