from fastapi import APIRouter, Body, HTTPException
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.models._stubs import CartItem

cart_router = APIRouter()


cart_router.post("")
def remove_book_from_cart(user_id: str = Body(..., embed=True), book_id: str = Body(..., embed=True)) -> None:
    """The book is removed from the user's shopping cart.

    Args:
        user_id: The unique identifier of the registered and logged-in user
        book_id: The unique identifier of the book to be removed from the shopping cart

    Returns:
        None.

    Raises:
        HTTPException: If the precondition is violated (The user is registered and logged-in; the book exists in the user's shopping cart).
    """
    db = SessionLocal()
    try:
        # Check if the cart item exists for the given user and book
        cart_item = db.query(CartItem).filter(
            CartItem.user_id == user_id,
            CartItem.book_id == book_id
        ).first()

        if not cart_item:
            raise HTTPException(status_code=404, detail="Book not found in the user's shopping cart.")

        # Remove the cart item
        db.delete(cart_item)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()