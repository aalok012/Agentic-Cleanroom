from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal


class ShoppingCart(Base):
    __tablename__ = "shopping_cart"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    book_title = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)


router = APIRouter()


def prompt_rental_period(user_id: str) -> dict[str, str]:
    """
    The system displays a form or interface requesting the user to specify the rental duration.

    Args:
        user_id: Unique identifier of the registered and logged-in user

    Returns:
        A form or interface requesting the user to specify the rental duration

    Raises:
        HTTPException: If the precondition is violated (The user has initiated the rent-out process and the system has confirmed the presence of books in the shopping cart).

    Notes:
        Precondition: The user has initiated the rent-out process and the system has confirmed the presence of books in the shopping cart
        Postcondition: The system waits for the user to input the rental period before proceeding to the next step
        Prerequisite: initiate_rental_process (req 4.6.REQ-1) must have run first.
    """
    # Check if user_id is provided
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    db = SessionLocal()
    try:
        # Check if there are items in the shopping cart for the user
        cart_items = (
            db.query(ShoppingCart)
            .filter(ShoppingCart.user_id == user_id)
            .all()
        )
        
        # If no items found, raise an exception
        if not cart_items:
            raise HTTPException(status_code=404, detail="No items found in the shopping cart")
        
        # Return the form for rental duration
        return {
            "form": "rental_duration_form",
            "fields": ["duration"]
        }
    finally:
        db.close()