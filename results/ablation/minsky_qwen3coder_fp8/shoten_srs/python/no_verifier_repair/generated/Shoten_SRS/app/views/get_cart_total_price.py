from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.controllers.calculate_and_display_rent import CartItem

class CartTotalPriceResponse(Base):
    total_price: float

router = APIRouter()


def get_cart_total_price(user_id: str) -> float:
    """
    The system displays the total price of all books currently in the shopping cart.

    Args:
        user_id: Unique identifier of the user whose cart total price is requested

    Returns:
        Total price of all books in the user's shopping cart

    Raises:
        HTTPException: If the precondition is violated (The user has items in their shopping cart).

    Notes:
        Precondition: The user has items in their shopping cart
        Postcondition: The displayed total price accurately reflects the sum of individual book prices in the cart
        canonical call (must work): {"user_id":"user123"}
        must return on success: 49.97
        error_mode: raise

        precondition failure call (must raise HTTPException with a 4xx status): {"user_id":""}
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID cannot be empty")

    db = SessionLocal()
    try:
        # Check if user has items in cart
        cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
        
        if not cart_items:
            raise HTTPException(status_code=404, detail="No items found in the user's shopping cart")
        
        # Calculate total price
        total_price = sum(item.price for item in cart_items)
        
        return total_price
    finally:
        db.close()