from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app.models.store_user_information import User
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app.controllers.validate_and_store_book_details import Book

router = APIRouter()

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app.controllers.calculate_and_display_rent import CartItem


def add_book_to_cart(user_id: str, book_id: str) -> None:
    """
    The book is added to the user's shopping cart list.

    Args:
        user_id: Unique identifier of the authenticated user adding the book
        book_id: Unique identifier of the book to be added to the cart

    Returns:
        None.

    Raises:
        HTTPException: If the precondition is violated (The user is authenticated and the book exists in the system).

    Notes:
        Precondition: The user is authenticated and the book exists in the system
        Postcondition: The user's shopping cart contains the added book and the system retains this information for the duration of the session
    """
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

        # Add book to cart
        cart_item = CartItem(user_id=user_id, book_id=book_id)
        db.add(cart_item)
        db.commit()
    finally:
        db.close()