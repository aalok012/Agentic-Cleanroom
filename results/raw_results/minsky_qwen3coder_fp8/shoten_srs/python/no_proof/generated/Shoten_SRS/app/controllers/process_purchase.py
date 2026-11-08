from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.controllers.calculate_and_display_rent import CartItem

router = APIRouter()

@router.post("")
def process_purchase(
    user_id: str = Body(..., embed=True),
    cart_items: list[dict[str, object]] = Body(..., embed=True)
) -> dict[str, object]:
    db = SessionLocal()
    try:
        # Validate preconditions
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        if not cart_items or len(cart_items) == 0:
            raise HTTPException(status_code=400, detail="Shopping cart cannot be empty")
        
        # Check if user exists in the database
        user_exists = db.query(CartItem).filter(CartItem.user_id == user_id).first()
        if not user_exists:
            raise HTTPException(status_code=403, detail="User is not registered or logged in")
        
        # Calculate total cost using the prerequisite function
        from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.models.calculate_shopping_cart_total import calculate_shopping_cart_total
        total_cost = calculate_shopping_cart_total(cart_items)
        
        # Mark items as purchased (in a real implementation, this would involve updating the DB)
        # For now, we'll simulate the purchase by returning the purchased items
        purchased_items = []
        for item in cart_items:
            purchased_items.append({
                "title": item["title"],
                "price": item["price"],
                "quantity": item["quantity"]
            })
        
        # Remove items from cart (in a real implementation, this would involve deleting from DB)
        # For now, we're just simulating the removal
        
        return {
            "status": "success",
            "purchased_items": purchased_items,
            "total_cost": round(total_cost, 2)
        }
    finally:
        db.close()