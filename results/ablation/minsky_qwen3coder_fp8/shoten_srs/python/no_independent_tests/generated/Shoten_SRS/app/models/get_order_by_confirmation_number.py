from fastapi import HTTPException, status
from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"extend_existing": True}
    
    confirmation_number = Column(String, primary_key=True)
    user_id = Column(String)
    order_id = Column(String)
    status = Column(String)
    shipping_date = Column(String)
    delivery_address = Column(String)
    projected_delivery_date = Column(String)

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
            "status": order.status,
            "shipping_date": order.shipping_date,
            "delivery_address": order.delivery_address,
            "projected_delivery_date": order.projected_delivery_date
        }
    finally:
        db.close()