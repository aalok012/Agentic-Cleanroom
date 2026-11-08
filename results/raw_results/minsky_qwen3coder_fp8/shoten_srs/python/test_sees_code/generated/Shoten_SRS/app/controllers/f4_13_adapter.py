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
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.extensions import Base, SessionLocal, engine

Base.metadata.create_all(engine)

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.controllers.f4_11_adapter import AppState

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_model(db: Session, key: str):
    state_row = db.query(AppState).filter(AppState.key == key).first()
    if state_row is None:
        return Dom.Init()
    return M.from_map(M.from_str(state_row.value), vconv=lambda x: M.from_map(x, vconv=lambda y: (M.from_str(y[0]), M.from_str(y[1]))))

def set_model(db: Session, key: str, model):
    json_value = M.to_str(M.to_map(model, vconv=lambda x: (M.to_str(x[0]), M.to_str(x[1]))))
    state_row = db.query(AppState).filter(AppState.key == key).first()
    if state_row is None:
        state_row = AppState(key=key, value=json_value)
        db.add(state_row)
    else:
        state_row.value = json_value
    db.commit()

@router.get("/users/{user_id}/purchase-history")
def get_user_purchase_history(user_id: str, days_back: int = 730, db: Session = Depends(get_db)):
    # Precondition: User is authenticated and authorized
    # This is a placeholder check - in real app, verify user auth
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    # Load current state
    model = get_model(db, f"user_{user_id}_state")
    
    # Apply action
    action = core.Action_ViewPurchaseHistory()
    new_state = Dom.Normalize(Dom.Apply(model, action))
    
    # Save updated state
    set_model(db, f"user_{user_id}_state", new_state)
    
    # Format response
    purchases = M.from_map(new_state[0], vconv=lambda x: (M.from_str(x[0]), M.from_str(x[1])))
    formatted_purchases = []
    for purchase_id, (date, payment_mode) in purchases.items():
        formatted_purchases.append({
            "date": date,
            "payment_mode": payment_mode
        })
    
    return formatted_purchases

@router.get("/users/{user_id}/orders/{order_id}")
def get_order_details(user_id: str, order_id: int, db: Session = Depends(get_db)):
    # Precondition: User is authenticated and authorized
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    # Load current state
    model = get_model(db, f"user_{user_id}_state")
    
    # Apply action
    action = core.Action_ViewOrderDetails(order_id)
    new_state = Dom.Normalize(Dom.Apply(model, action))
    
    # Save updated state
    set_model(db, f"user_{user_id}_state", new_state)
    
    # Format response
    orders = M.from_map(new_state[1], vconv=lambda x: M.from_map(x, vconv=lambda y: (int(y[0]), int(y[1]))))
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    
    items = orders[order_id]
    formatted_items = []
    for title, (price, quantity) in items.items():
        formatted_items.append({
            "title": title,
            "price": price,
            "quantity": quantity
        })
    
    return formatted_items

@router.post("/users/{user_id}/purchases")
def add_purchase(user_id: str, purchase: dict, db: Session = Depends(get_db)):
    # Precondition: User is authenticated and authorized
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    # Load current state
    model = get_model(db, f"user_{user_id}_state")
    
    # Create new purchase
    new_purchase = core.Purchase(
        M.to_str(purchase["date"]),
        M.to_str(purchase["payment_mode"])
    )
    
    # Update model with new purchase
    new_purchases = M.from_map(model[0], vconv=lambda x: (M.from_str(x[0]), M.from_str(x[1])))
    new_purchases[len(new_purchases)] = (purchase["date"], purchase["payment_mode"])
    
    new_orders = M.from_map(model[1], vconv=lambda x: M.from_map(x, vconv=lambda y: (int(y[0]), int(y[1]))))
    
    new_model = (M.to_map(new_purchases, vconv=lambda x: (M.to_str(x[0]), M.to_str(x[1]))), M.to_map(new_orders))
    
    # Save updated state
    set_model(db, f"user_{user_id}_state", new_model)
    
    return {"message": "Purchase added successfully"}

@router.post("/users/{user_id}/orders")
def add_order(user_id: str, order: dict, db: Session = Depends(get_db)):
    # Precondition: User is authenticated and authorized
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    # Load current state
    model = get_model(db, f"user_{user_id}_state")
    
    # Create new order
    items = {}
    for item in order["items"]:
        items[item["title"]] = (item["price"], item["quantity"])
    
    new_order = M.to_map(items, vconv=lambda x: (M.to_str(x[0]), M.to_str(x[1])))
    
    # Update model with new order
    new_purchases = M.from_map(model[0], vconv=lambda x: (M.from_str(x[0]), M.from_str(x[1])))
    new_orders = M.from_map(model[1], vconv=lambda x: M.from_map(x, vconv=lambda y: (int(y[0]), int(y[1]))))
    new_orders[len(new_orders)] = new_order
    
    new_model = (M.to_map(new_purchases, vconv=lambda x: (M.to_str(x[0]), M.to_str(x[1]))), M.to_map(new_orders))
    
    # Save updated state
    set_model(db, f"user_{user_id}_state", new_model)
    
    return {"message": "Order added successfully"}