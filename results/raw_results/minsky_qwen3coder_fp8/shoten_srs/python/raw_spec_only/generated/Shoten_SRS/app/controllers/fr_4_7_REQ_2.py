from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_9_REQ_2 import Book
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.models._stubs import Cart

table_name = "cart_items"

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.models._stubs import CartItem

router = APIRouter()


def fr_4_7_REQ_2(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Get all items in the cart
        cart_items = db.query(CartItem).all()
        
        # Calculate total cost
        total_cost = 0.0
        for item in cart_items:
            total_cost += item.price * item.quantity
        
        return {"total_cost": total_cost}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()