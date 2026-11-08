from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class ShoppingCart(Base):
    __tablename__ = "shopping_cart"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    book_title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    rented = Column(Boolean, default=False)

router = APIRouter()


def prompt_rental_period_input(user_id: str) -> dict[str, str]:
    """
    The system displays a form or interface requesting the user to specify the rental duration.

    Args:
        user_id: Unique identifier of the registered and logged-in user who initiated the rental process

    Returns:
        A dictionary containing the prompt message and form fields for rental period input

    Raises:
        HTTPException: If the precondition is violated (The user has initiated the rent-out process and the system has confirmed the presence of books in the shopping cart).
    """
    # Check if user_id is provided
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Open database session
    db = SessionLocal()
    try:
        # Check if the user has items in the shopping cart
        cart_items = db.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).all()
        
        # If no items found, raise an exception
        if not cart_items:
            raise HTTPException(status_code=404, detail="No items found in the shopping cart")
        
        # Return the prompt and form fields
        return {
            "prompt": "Please enter the rental period",
            "form_fields": ["duration"]
        }
    finally:
        db.close()