from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.models._stubs import Cart
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.controllers.validate_and_store_book_details import Book

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.controllers.calculate_and_display_rent import CartItem

router = APIRouter()

@router.post("")
def get_cart_total_price(user_id: str = Body(..., embed=True)) -> float:
    db = SessionLocal()
    try:
        # Check if user has items in cart
        cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
        if not cart_items:
            raise HTTPException(status_code=404, detail="User has no items in shopping cart")
        
        total_price = 0.0
        for item in cart_items:
            # Get book details to calculate price
            book = db.query(Book).filter(Book.id == item.book_id).first()
            if book:
                total_price += book.price * item.quantity
        
        return round(total_price, 2)
    finally:
        db.close()