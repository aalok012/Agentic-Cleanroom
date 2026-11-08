from fastapi import HTTPException
from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.models.get_user_orders_last_30_days import Order
    

def get_order_by_confirmation_number(confirmation_number: str, user_id: str) -> dict[str, str]:
    db = SessionLocal()
    try:
        order = db.query(Order).filter(
            Order.confirmation_number == confirmation_number,
            Order.user_id == user_id
        ).first()
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return {
            "order_id": order.order_id,
            "confirmation_number": order.confirmation_number,
            "status": order.status
        }
    finally:
        db.close()