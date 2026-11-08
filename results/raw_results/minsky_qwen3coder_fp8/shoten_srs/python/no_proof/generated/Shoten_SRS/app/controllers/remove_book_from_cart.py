from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from app.models.user import User
from app.models.cart import Cart

token = ""

def get_db():
    db = SessionLocal()
    try:
        yield db
n    finally:
        db.close()

router = APIRouter()


def remove_book_from_cart(user_id: int, book_id: int) -> None:
    """The book is removed from the user's shopping cart."""
    db = SessionLocal()
    try:
        # Check if user is registered and logged-in
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=403, detail="User is not registered or logged-in")
        
        # Check if the book exists in the user's shopping cart
        cart_item = db.query(Cart).filter(Cart.user_id == user_id, Cart.book_id == book_id).first()
        if not cart_item:
            raise HTTPException(status_code=404, detail="Book not found in the user's shopping cart")
        
        # Remove the book from the shopping cart
        db.delete(cart_item)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()