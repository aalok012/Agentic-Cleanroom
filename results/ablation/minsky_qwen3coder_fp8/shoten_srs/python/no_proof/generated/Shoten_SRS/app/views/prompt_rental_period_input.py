from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class ShoppingCart(Base):
    __tablename__ = "shopping_cart"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    book_title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    rented = Column(Boolean, default=False)

router = APIRouter()

@router.post("")
def prompt_rental_period_input(user_id: str = Body(..., embed=True)) -> dict[str, str]:
    # Open database session
    db = SessionLocal()
    try:
        # Validate precondition: user has initiated rental process and has items in cart
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID cannot be empty")
        
        # Check if user has items in the shopping cart
        cart_items = db.query(ShoppingCart).filter(ShoppingCart.user_id == user_id).all()
        if not cart_items:
            raise HTTPException(status_code=404, detail="No items found in the shopping cart")
        
        # Return the prompt and form fields
        return {
            "prompt": "Please enter the rental period",
            "form_fields": ["duration"]
        }
    finally:
        db.close()