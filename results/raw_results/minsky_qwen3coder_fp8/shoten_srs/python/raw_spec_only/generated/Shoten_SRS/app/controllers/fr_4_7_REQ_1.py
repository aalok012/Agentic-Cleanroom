from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_1_REQ_2 import User
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.models._stubs import Cart
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_9_REQ_2 import Book

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_4_REQ_2 import CartItemModel as CartItem

router = APIRouter()


def fr_4_7_REQ_1(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Check if user is logged in (assuming user_id is in request or session)
        # For simplicity, we'll assume user_id is passed in request
        if "user_id" not in request:
            raise HTTPException(status_code=403, detail="User not authenticated")
        
        user_id = request["user_id"]
        
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get all items in user's cart
        cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
        if not cart_items:
            raise HTTPException(status_code=400, detail="Shopping cart is empty")
        
        # Process each item in the cart
        for item in cart_items:
            book = db.query(Book).filter(Book.id == item.book_id).first()
            if not book:
                raise HTTPException(status_code=404, detail="Book not found")
            
            # Check if enough stock
            if book.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Not enough stock for {book.title}")
            
            # Deduct stock
            book.stock -= item.quantity
            
            # In a real system, here we would process payment and create order records
            # For now, we just remove the item from cart
            
        # Clear the cart after successful purchase
        db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        db.commit()
        
        return {}
    except HTTPException:
        db.rollback()
        raise
    finally:
        db.close()