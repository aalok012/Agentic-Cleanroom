import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F4_6-py"))
import dafny_marshal as M
import F4__6Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import SessionLocal, engine, Base
from sqlalchemy import Column, Integer, String, Text
import json

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.f4_10_adapter import AppState

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/feature46", tags=["feature46"])

def get_state(db: Session) -> Dom.Model:
    state_row = db.query(AppState).filter(AppState.key == "rent_state").first()
    if state_row is None:
        return Dom.Init()
    return M.from_seq(json.loads(state_row.value), lambda x: M.from_map(x, vconv=int))

def save_state(db: Session, state: Dom.Model):
    value = M.to_seq(state, lambda x: M.to_map(x, vconv=lambda y: str(y)))
    json_value = json.dumps(value)
    state_row = db.query(AppState).filter(AppState.key == "rent_state").first()
    if state_row is None:
        state_row = AppState(key="rent_state", value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()

@router.post("/req1")
def fr_4_6_REQ_1(request: dict, db: Session = Depends(get_db)):
    state = get_state(db)
    action = core.Action_RentBooks()
    new_state = Dom.Normalize(Dom.Apply(state, action))
    save_state(db, new_state)
    return {"message": "System allows user to rent books in cart"}

@router.post("/req2")
def fr_4_6_REQ_2(request: dict, db: Session = Depends(get_db)):
    if "period" not in request:
        raise HTTPException(status_code=400, detail="Missing period in request")
    
    state = get_state(db)
    action = core.Action_EnterRentalPeriod(M.to_str(request["period"]))
    new_state = Dom.Normalize(Dom.Apply(state, action))
    save_state(db, new_state)
    return {"message": "User prompted to enter rental period"}

@router.post("/req3")
def fr_4_6_REQ_3(request: dict, db: Session = Depends(get_db)):
    state = get_state(db)
    action = core.Action_DisplayRentCharges()
    new_state = Dom.Normalize(Dom.Apply(state, action))
    save_state(db, new_state)
    # Extract rent charges from state
    _, rent_charges, _, _, _, _, _ = new_state
    return {"rent_charges": M.from_map(rent_charges, vconv=int)}

@router.post("/req4")
def fr_4_6_REQ_4(request: dict, db: Session = Depends(get_db)):
    if "delivery_info" not in request:
        raise HTTPException(status_code=400, detail="Missing delivery_info in request")
    
    state = get_state(db)
    action = core.Action_EnterDeliveryInfo(M.to_str(request["delivery_info"]))
    new_state = Dom.Normalize(Dom.Apply(state, action))
    save_state(db, new_state)
    return {"message": "User delivery info entered"}

@router.post("/req5")
def fr_4_6_REQ_5(request: dict, db: Session = Depends(get_db)):
    if "payment_info" not in request:
        raise HTTPException(status_code=400, detail="Missing payment_info in request")
    
    state = get_state(db)
    action = core.Action_EnterPaymentInfo(M.to_str(request["payment_info"]))
    new_state = Dom.Normalize(Dom.Apply(state, action))
    save_state(db, new_state)
    return {"message": "User payment info entered"}

@router.post("/req6")
def fr_4_6_REQ_6(request: dict, db: Session = Depends(get_db)):
    state = get_state(db)
    action = core.Action_ConfirmTransaction()
    new_state = Dom.Normalize(Dom.Apply(state, action))
    save_state(db, new_state)
    # Extract cart from state
    cart, _, _, _, _, _, _ = new_state
    return {"books": M.from_map(cart, vconv=int)}