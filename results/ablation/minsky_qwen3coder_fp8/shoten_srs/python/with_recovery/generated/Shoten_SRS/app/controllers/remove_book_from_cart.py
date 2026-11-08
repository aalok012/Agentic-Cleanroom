from fastapi import APIRouter, Body, HTTPException
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.models.store_user_information import User
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.models._stubs import Cart

router = APIRouter()

def remove_book_from_cart(user_id: int, book_id: int) -> None:
    """The book is removed from the user's shopping cart.

    Args:
        user_id: The unique identifier of the registered and logged-in user
        book_id: The unique identifier of the book to be removed from the shopping cart

    Raises:
        HTTPException: If the precondition is violated (The user is registered and logged-in; the book exists in the user's shopping cart).
    """
    db = SessionLocal()
    try:
        # Check if user exists and is logged in
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the book exists in the user's cart
        cart_item = db.query(Cart).filter(
            Cart.user_id == user_id,
            Cart.book_id == book_id
        ).first()
        if not cart_item:
            raise HTTPException(status_code=404, detail="Book not found in cart")

        # Remove the book from the cart
        db.delete(cart_item)
        db.commit()
    finally:
        db.close()