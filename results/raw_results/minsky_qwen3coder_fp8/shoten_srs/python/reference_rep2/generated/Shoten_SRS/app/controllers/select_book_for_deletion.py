from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.models._stubs import Cart

router = APIRouter()

def select_book_for_deletion(user_id: str, book_id: str) -> dict[str, str]:
    """
    The system identifies the selected book for deletion.

    Args:
        user_id: The unique identifier of the registered and logged-in user
        book_id: The unique identifier of the book selected for deletion

    Returns:
        A confirmation message indicating the book has been selected for deletion

    Raises:
        HTTPException: If the precondition is violated (The user is registered and logged-in; the selected book exists in the user's shopping cart).
    """
    db = SessionLocal()
    try:
        # Check if the user is registered and logged-in (basic check)
        if not user_id:
            raise HTTPException(status_code=403, detail="User is not authenticated")
        
        # Check if the book exists in the user's shopping cart
        cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.book_id == book_id).first()
        
        if not cart_item:
            raise HTTPException(status_code=404, detail="Book not found in the user's shopping cart")
        
        # If we reach here, the book exists in the cart
        return {"message": "Book selected for deletion"}
    finally:
        db.close()