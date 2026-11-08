from fastapi import APIRouter, Body, HTTPException
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.controllers.calculate_and_display_rent import CartItem

router = APIRouter()


def update_cart_after_deletion(user_id: int, book_id: int) -> list[dict[str, int]]:
    """
    The stored list representing the shopping cart is updated by removing the specified book,
    and the display is updated to show only the remaining books in the cart.

    Args:
        user_id: The unique identifier of the registered and logged-in user
        book_id: The unique identifier of the book to be deleted from the shopping cart

    Returns:
        The updated list of books in the shopping cart after deletion

    Raises:
        HTTPException: If the precondition is violated (The user is registered and logged-in;
        the specified book exists in the user's shopping cart).
    """
    db = SessionLocal()
    try:
        # Check if the user is registered and logged-in
        # This is a placeholder check; actual implementation would verify user session
        # For now, we assume the user is valid based on the preconditions
        
        # Check if the book exists in the user's cart
        cart_item = db.query(CartItem).filter(
            CartItem.user_id == user_id,
            CartItem.book_id == book_id
        ).first()
        
        if not cart_item:
            raise HTTPException(status_code=404, detail="Book not found in the user's shopping cart")
        
        # Remove the book from the cart
        db.delete(cart_item)
        db.commit()
        
        # Retrieve the updated cart
        updated_cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
        
        # Format the response
        result = []
        for item in updated_cart_items:
            result.append({
                "book_id": item.book_id,
                "title": item.title  # Assuming title is stored in the model
            })
        
        return result
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()