from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"extend_existing": True}
    confirmation_number = Column(String, primary_key=True)
    shipping_status = Column(String)

router = APIRouter()


def fr_4_12_REQ_2(request: dict) -> dict:
    db = SessionLocal()
    try:
        confirmation_number = request.get("confirmation_number")
        if not confirmation_number:
            raise HTTPException(status_code=400, detail="Confirmation number is required.")
        
        order = db.query(Order).filter(Order.confirmation_number == confirmation_number).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found.")
        
        return {"shipping_status": order.shipping_status}
    finally:
        db.close()