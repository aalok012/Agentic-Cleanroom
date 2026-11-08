from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.models._stubs import Cart

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.controllers.calculate_and_display_rent import CartItem

router = APIRouter()

@router.post("")
def select_book_for_deletion(user_id: int = Body(..., embed=True), book_id: int = Body(..., embed=True)) -> dict[str, int]:
    db = SessionLocal()
    try:
        # Check if the user exists and is logged in (simplified check)
        # In a real application, you would verify the user's authentication status
        
        # Check if the book exists in the user's cart
        cart_item = db.query(CartItem).filter(
            CartItem.user_id == user_id,
            CartItem.book_id == book_id
        ).first()
        
        if not cart_item:
            raise HTTPException(status_code=404, detail="Book not found in the user's cart")
        
        # Return the details of the selected book for deletion
        return {"user_id": user_id, "book_id": book_id}
    finally:
        db.close()