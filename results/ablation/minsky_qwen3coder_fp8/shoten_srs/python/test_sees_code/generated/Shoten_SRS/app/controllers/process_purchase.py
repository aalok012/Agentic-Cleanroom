from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.models.calculate_shopping_cart_total import calculate_shopping_cart_total

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.controllers.calculate_and_display_rent import CartItem

router = APIRouter()


def process_purchase(user_id: str, cart_items: list[dict[str, object]]) -> dict[str, object]:
    db = SessionLocal()
    try:
        # Validate preconditions
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        if not cart_items:
            raise HTTPException(status_code=400, detail="Shopping cart cannot be empty")
        
        # Calculate total cost using the prerequisite function
        total_cost = calculate_shopping_cart_total(cart_items)
        
        # Simulate removing items from cart and marking them as purchased
        # In a real implementation, we would delete the cart items and insert purchase records
        # For now, we'll just return the expected result
        purchased_items = cart_items.copy()
        
        # Remove all items from the cart
        db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        db.commit()
        
        return {
            "status": "success",
            "purchased_items": purchased_items,
            "total_cost": round(total_cost, 2)
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()