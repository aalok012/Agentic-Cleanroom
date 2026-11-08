from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.models.get_order_by_confirmation_number import Order

router = APIRouter()

@router.post("")
def display_order_shipping_details(order: dict[str, str] = Body(..., embed=True)) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if order exists and user has access
        if not order or "shipping_date" not in order or "delivery_address" not in order or "projected_delivery_date" not in order or "status" not in order:
            raise HTTPException(status_code=400, detail="Order does not exist or user does not have access")
        
        # Return formatted shipping details
        return {
            "shipping_date": order["shipping_date"],
            "delivery_address": order["delivery_address"],
            "projected_delivery_date": order["projected_delivery_date"],
            "status": order["status"]
        }
    finally:
        db.close()