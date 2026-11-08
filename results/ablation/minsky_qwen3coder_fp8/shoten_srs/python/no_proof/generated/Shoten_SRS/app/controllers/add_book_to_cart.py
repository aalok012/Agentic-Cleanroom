from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.models.store_user_information import User
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.controllers.validate_and_store_book_details import Book

type: ignore

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.controllers.calculate_and_display_rent import CartItem

router = APIRouter()

@router.post("")
def add_book_to_cart(
    user_id: str = Body(..., embed=True),
    book_id: str = Body(..., embed=True)
) -> None:
    db = SessionLocal()
    try:
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=403, detail="User is not authenticated")
        
        # Check if book exists
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Create cart item
        cart_item = CartItem(user_id=user_id, book_id=book_id)
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()