from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from datetime import datetime, timedelta

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.models.get_order_by_confirmation_number import Order

router = APIRouter()


def get_user_orders_in_last_30_days(user_id: str) -> list[dict[str, str]]:
    db = SessionLocal()
    try:
        # Check if user is registered and logged in (basic check)
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID cannot be empty")

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