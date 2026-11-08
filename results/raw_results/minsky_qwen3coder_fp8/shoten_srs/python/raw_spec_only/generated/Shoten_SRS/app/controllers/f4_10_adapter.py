import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F4_10-py"))
import dafny_marshal as M
import F4__10Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal, engine

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

def load_state(db: Session) -> Dom.Model:
    row = db.query(AppState).filter(AppState.key == "state").first()
    if row is None:
        return Dom.Init()
    return M.from_seq(M.from_str(row.value), lambda x: M.from_str(x))

def save_state(db: Session, state: Dom.Model):
    json_value = M.to_str(M.to_seq(state, lambda x: M.to_str(x)))
    row = db.query(AppState).filter(AppState.key == "state").first()
    if row is None:
        db.add(AppState(key="state", value=json_value))
    else:
        row.value = json_value
    db.commit()

def fr_4_10_REQ_1(request: dict) -> dict:
    with next(get_db_session()) as db:
        model = load_state(db)
        action = core.Action_ViewContactInfo()
        new_model = Dom.Normalize(Dom.Apply(model, action))
        save_state(db, new_model)
        
        # Extract fields from the model
        (bookstoreAddr, bookstorePhone, bookstoreEmail, printstoreAddr, printstorePhone, printstoreEmail,
         studentAddr, studentPhone, studentEmail, bookstoreDir, printstoreDir, studentDir) = new_model
        
        return {
            "bookstore": {
                "address": M.from_str(bookstoreAddr),
                "phone": M.from_str(bookstorePhone),
                "email": M.from_str(bookstoreEmail)
            },
            "printstore": {
                "address": M.from_str(printstoreAddr),
                "phone": M.from_str(printstorePhone),
                "email": M.from_str(printstoreEmail)
            },
            "student": {
                "address": M.from_str(studentAddr),
                "phone": M.from_str(studentPhone),
                "email": M.from_str(studentEmail)
            }
        }

def fr_4_10_REQ_2(request: dict) -> dict:
    with next(get_db_session()) as db:
        model = load_state(db)
        action = core.Action_DisplayStoreDetails()
        new_model = Dom.Normalize(Dom.Apply(model, action))
        save_state(db, new_model)
        
        # Extract fields from the model
        (bookstoreAddr, bookstorePhone, bookstoreEmail, printstoreAddr, printstorePhone, printstoreEmail,
         studentAddr, studentPhone, studentEmail, bookstoreDir, printstoreDir, studentDir) = new_model
        
        return {
            "bookstore": {
                "address": M.from_str(bookstoreAddr),
                "phone": M.from_str(bookstorePhone),
                "email": M.from_str(bookstoreEmail),
                "directions": M.from_str(bookstoreDir)
            },
            "printstore": {
                "address": M.from_str(printstoreAddr),
                "phone": M.from_str(printstorePhone),
                "email": M.from_str(printstoreEmail),
                "directions": M.from_str(printstoreDir)
            },
            "student": {
                "address": M.from_str(studentAddr),
                "phone": M.from_str(studentPhone),
                "email": M.from_str(studentEmail),
                "directions": M.from_str(studentDir)
            }
        }

def fr_4_10_REQ_3(request: dict) -> dict:
    with next(get_db_session()) as db:
        model = load_state(db)
        action = core.Action_ShowMap()
        new_model = Dom.Normalize(Dom.Apply(model, action))
        save_state(db, new_model)
        
        # Extract fields from the model
        (bookstoreAddr, bookstorePhone, bookstoreEmail, printstoreAddr, printstorePhone, printstoreEmail,
         studentAddr, studentPhone, studentEmail, bookstoreDir, printstoreDir, studentDir) = new_model
        
        return {
            "map": {
                "bookstore": {
                    "address": M.from_str(bookstoreAddr),
                    "directions": M.from_str(bookstoreDir)
                },
                "printstore": {
                    "address": M.from_str(printstoreAddr),
                    "directions": M.from_str(printstoreDir)
                }
            }
        }