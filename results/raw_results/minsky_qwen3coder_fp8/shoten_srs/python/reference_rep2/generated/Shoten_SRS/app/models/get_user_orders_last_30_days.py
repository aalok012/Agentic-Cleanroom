from fastapi import APIRouter, Body, HTTPException, status
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from datetime import datetime, timedelta

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, index=True)
    user_id = Column(String, index=True)
    status = Column(String)
    created_at = Column(DateTime)

router = APIRouter()


def get_user_orders_last_30_days(user_id: str) -> list[dict[str, str]]:
    db = SessionLocal()
    try:
        # Check if user exists (precondition)
        # In a real app, you'd check if the user is authenticated
        # For now, we assume the user is authenticated if the ID is provided
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")

        # Calculate the date 30 days ago
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)

        # Query orders for the user within the last 30 days
        orders = db.query(Order).filter(
            Order.user_id == user_id,
            Order.created_at >= thirty_days_ago
        ).all()

        # Convert to list of dictionaries
        result = []
        for order in orders:
            result.append({
                "order_id": order.order_id,
                "status": order.status
            })

        return result
    finally:
        db.close()