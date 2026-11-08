from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_1_REQ_2 import User
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_9_REQ_2 import Book
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.models._stubs import Wishlist

router = APIRouter()

class WishlistItem(Base):
    __tablename__ = "wishlist_items"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    book_id = Column(Integer, nullable=False)


def fr_4_4_REQ_1(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Extract user_id and book_id from request
        user_id = request.get("user_id")
        book_id = request.get("book_id")
        
        if not user_id or not book_id:
            raise HTTPException(status_code=400, detail="Missing user_id or book_id")
        
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if book exists
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Create wishlist item
        wishlist_item = WishlistItem(user_id=user_id, book_id=book_id)
        db.add(wishlist_item)
        db.commit()
        db.refresh(wishlist_item)
        
        return {}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()