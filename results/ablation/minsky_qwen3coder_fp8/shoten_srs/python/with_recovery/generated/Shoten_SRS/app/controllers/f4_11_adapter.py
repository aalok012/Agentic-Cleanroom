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

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.extensions import Base, SessionLocal, engine

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


def get_model(db: Session, user_id: str) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == user_id).first()
    if state_row is None:
        return Dom.Init()
    return M.from_seq(M.from_str(state_row.value), lambda x: M.from_str(x))


def save_model(db: Session, user_id: str, model: Dom.Model) -> None:
    json_value = M.to_str(M.to_seq(M.from_seq(model, lambda x: M.to_str(x)), lambda x: M.to_str(x)))
    state_row = db.query(AppState).filter(AppState.key == user_id).first()
    if state_row is None:
        new_row = AppState(key=user_id, value=json_value)
        db.add(new_row)
    else:
        state_row.value = json_value
    db.commit()


def initiate_account_update(user_id: str, update_data: dict) -> None:
    pass


def update_user_details(user_id: str, name: str, mailing_address: str, billing_address: str, payment_info: dict) -> bool:
    db = next(get_db_session())
    model = get_model(db, user_id)
    action = core.Action_UpdateAccountInfo(
        M.to_str(name),
        M.to_str(mailing_address),
        M.to_str(billing_address),
        M.to_str(str(payment_info))
    )
    new_model = Dom.Normalize(Dom.Apply(model, action))
    save_model(db, user_id, new_model)
    return True


def change_password(user_id: str, old_password: str, new_password: str, confirm_new_password: str) -> bool:
    db = next(get_db_session())
    model = get_model(db, user_id)
    action = core.Action_ChangePassword(
        M.to_str(old_password),
        M.to_str(new_password),
        M.to_str(confirm_new_password)
    )
    new_model = Dom.Normalize(Dom.Apply(model, action))
    save_model(db, user_id, new_model)
    return True