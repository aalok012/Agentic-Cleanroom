from fastapi import APIRouter, Body, HTTPException
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app.controllers.calculate_and_display_rent import CartItem

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app.controllers.calculate_and_display_rent import CartItem as CartItemModel

router = APIRouter()


def remove_book_from_cart(user_id: int, book_id: int) -> None:
    db = SessionLocal()
    try:
        cart_item = db.query(CartItemModel).filter(
            CartItemModel.user_id == user_id,
            CartItemModel.book_id == book_id
        ).first()
        if cart_item:
            db.delete(cart_item)
            db.commit()
    finally:
        db.close()


def select_book_for_deletion(user_id: int, book_id: int) -> dict[str, int]:
    db = SessionLocal()
    try:
        cart_item = db.query(CartItemModel).filter(
            CartItemModel.user_id == user_id,
            CartItemModel.book_id == book_id
        ).first()
        if not cart_item:
            raise HTTPException(status_code=404, detail="Book not found in cart")
        return {"book_id": cart_item.book_id}
    finally:
        db.close()


@router.post("")
def update_cart_after_deletion(user_id: int = Body(..., embed=True), book_id: int = Body(..., embed=True)) -> list[dict[str, int]]:
    # Check preconditions
    select_book_for_deletion(user_id, book_id)
    
    # Remove the book from the cart
    remove_book_from_cart(user_id, book_id)
    
    # Retrieve updated cart
    db = SessionLocal()
    try:
        cart_items = db.query(CartItemModel).filter(CartItemModel.user_id == user_id).all()
        return [
            {"book_id": item.book_id}
            for item in cart_items
        ]
    finally:
        db.close()