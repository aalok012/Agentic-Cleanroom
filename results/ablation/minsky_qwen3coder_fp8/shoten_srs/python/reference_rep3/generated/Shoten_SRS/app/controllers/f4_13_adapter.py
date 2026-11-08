import os, sys
_d = os.path.dirname(os.path.abspath(__file__))
while _d != os.path.dirname(_d) and not os.path.isdir(os.path.join(_d, "dafny_cores")):
    _d = os.path.dirname(_d)
_CORES = os.path.join(_d, "dafny_cores")
sys.path.insert(0, _CORES)
sys.path.insert(0, os.path.join(_CORES, "F4_13-py"))
import dafny_marshal as M
import F4__13Domain as core
Dom = core.default__

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import SessionLocal, engine, Base
from sqlalchemy import Column, Integer, String, Text
import json

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.controllers.f4_11_adapter import AppState

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/purchase-history", tags=["purchase-history"])


def get_user_purchase_history(user_id: str, days_back: int = 730) -> list[dict[str, object]]:
    db: Session = next(get_db())
    
    # Load existing state or initialize
    state_row = db.query(AppState).filter(AppState.key == f"user_{user_id}_state").first()
    if state_row:
        model_dict = json.loads(state_row.value)
        model = M.from_map(model_dict, vconv=lambda x: (x[0], x[1]))
    else:
        model = Dom.Init()
    
    # Create action
    action = core.Action_ViewPurchaseHistory()
    
    # Apply action
    new_state = Dom.Normalize(Dom.Apply(model, action))
    
    # Save updated state
    new_state_json = json.dumps(M.to_map(new_state, kconv=M.to_str, vconv=lambda x: (x[0], x[1])))
    if state_row:
        state_row.value = new_state_json
    else:
        state_row = AppState(key=f"user_{user_id}_state", value=new_state_json)
        db.add(state_row)
    db.commit()
    
    # Return purchases
    purchases = new_state[0]
    result = []
    for purchase_id, purchase in purchases.items():
        result.append({
            "date": purchase[0],
            "paymentMode": purchase[1]
        })
    return result


def format_purchase_summary(purchase: dict[str, object]) -> dict[str, object]:
    return {
        "date": purchase["date"],
        "paymentMode": purchase["paymentMode"]
    }


def format_order_books(order: dict[str, object]) -> list[dict[str, object]]:
    books = []
    for title, (price, quantity) in order["items"].items():
        books.append({
            "title": title,
            "price": price,
            "quantity": quantity
        })
    return books