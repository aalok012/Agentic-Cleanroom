from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.models.get_user_orders_last_30_days import Order

router = APIRouter()

def get_order_shipping_details(order_id: str) -> dict[str, str]:
    """
    The system presents the shipping date, mailing address, projected delivery date,
    and status (in transit, delivered, etc.) for the selected order.

    Args:
        order_id: The unique identifier of the order for which shipping details are requested

    Returns:
        Shipping date, mailing address, projected delivery date, and status of the order

    Raises:
        HTTPException: If the precondition is violated (The order exists and the user has access to it based on the confirmation number or previous selection).
    """
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return {
            "shipping_date": order.shipping_date,
            "mailing_address": order.mailing_address,
            "projected_delivery_date": order.projected_delivery_date,
            "status": order.status
        }
    finally:
        db.close()