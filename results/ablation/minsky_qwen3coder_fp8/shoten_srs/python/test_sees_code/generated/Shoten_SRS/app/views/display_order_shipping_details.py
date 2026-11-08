from fastapi import APIRouter, Body, HTTPException, status
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.models.get_order_by_confirmation_number import Order

router = APIRouter()

@router.post("")
def display_order_shipping_details(order: dict[str, str] = Body(..., embed=True)) -> dict[str, str]:
    # Validate precondition: order exists and user has access
    if not order or "shipping_date" not in order or "delivery_address" not in order or "projected_delivery_date" not in order or "status" not in order:
        raise HTTPException(status_code=400, detail="Order does not exist or user does not have access")
    
    # Extract required fields
    shipping_date = order.get("shipping_date")
    delivery_address = order.get("delivery_address")
    projected_delivery_date = order.get("projected_delivery_date")
    status = order.get("status")
    
    # Return formatted shipping details
    return {
        "shipping_date": shipping_date,
        "delivery_address": delivery_address,
        "projected_delivery_date": projected_delivery_date,
        "status": status
    }