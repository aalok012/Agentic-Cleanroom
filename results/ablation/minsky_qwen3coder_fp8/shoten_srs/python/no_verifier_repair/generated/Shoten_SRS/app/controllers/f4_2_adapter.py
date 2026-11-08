import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F4_2-py"))
import dafny_marshal as M
import F4__2Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal, engine

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

def get_current_model(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "login_state").first()
    if state_row is None:
        return Dom.Init()
    return M.from_seq(M.from_str(state_row.value), lambda x: (x[0], x[1]))

def save_model(db: Session, model: Dom.Model) -> None:
    json_value = M.to_str(M.to_seq(model, lambda x: (M.to_str(x[0]), M.to_str(x[1]))))
    state_row = db.query(AppState).filter(AppState.key == "login_state").first()
    if state_row is None:
        state_row = AppState(key="login_state", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/login")
def login_user(username: str, password: str):
    with next(get_db_session()) as db:
        model = get_current_model(db)
        action = core.Action_Login(M.to_str(username), M.to_str(password))
        new_model = Dom.Normalize(Dom.Apply(model, action))
        save_model(db, new_model)
        return {"success": new_model[0]}

@router.post("/validate")
def validate_login_credentials(username: str, password: str):
    if not username or not password:
        raise HTTPException(status_code=400, detail="Both username and password are required.")
    return {}

@router.post("/verify")
def verify_credentials(username: str, password: str):
    with next(get_db_session()) as db:
        model = get_current_model(db)
        action = core.Action_Login(M.to_str(username), M.to_str(password))
        new_model = Dom.Normalize(Dom.Apply(model, action))
        save_model(db, new_model)
        return {"logged_in": new_model[0], "username": M.from_str(new_model[1])}
