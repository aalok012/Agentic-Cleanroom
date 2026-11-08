from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.controllers.calculate_and_display_rent import CartItem

class CartTotalPriceView:
    router = APIRouter()

    @staticmethod
    @router.post("")
    def get_cart_total_price(user_id: str = Body(..., embed=True)) -> float:
        db = SessionLocal()
        try:
            if not user_id:
                raise HTTPException(status_code=400, detail="User ID cannot be empty")
            
            # Check if user has items in cart
            cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
            if not cart_items:
                raise HTTPException(status_code=404, detail="User has no items in shopping cart")
            
            # Calculate total price
            total_price = sum(item.price * item.quantity for item in cart_items)
            return round(total_price, 2)
        finally:
            db.close()