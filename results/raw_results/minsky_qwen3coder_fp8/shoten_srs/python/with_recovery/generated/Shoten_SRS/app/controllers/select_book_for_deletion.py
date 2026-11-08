from fastapi import APIRouter, Body, HTTPException
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.extensions import SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.models._stubs import Cart

router = APIRouter()

def select_book_for_deletion(user_id: int, book_id: int) -> dict[str, int]:
    """
    The system identifies the selected book for deletion.

    Args:
        user_id: The unique identifier of the registered and logged-in user
        book_id: The unique identifier of the book selected for deletion

    Returns:
        The details of the selected book for deletion

    Raises:
        HTTPException: If the precondition is violated (The user is registered and logged-in; the selected book exists in the user's shopping cart).
    """
    db = SessionLocal()
    try:
        # Check if the user is registered and logged-in (simplified check)
        if user_id <= 0:
            raise HTTPException(status_code=403, detail="User is not registered or logged-in")
        
        # Check if the book exists in the user's shopping cart
        cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.book_id == book_id).first()
        
        if not cart_item:
            raise HTTPException(status_code=404, detail="Book not found in the user's shopping cart")
        
        # Return the details of the selected book for deletion
        return {"user_id": user_id, "book_id": book_id}
    finally:
        db.close()