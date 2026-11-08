from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.models.store_user_information import User

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.controllers.validate_and_store_book_details import Book

router = APIRouter()

@router.post("")
def initiate_rental_process(user_id: str = Body(..., embed=True), cart_items: list[dict[str, str]] = Body(..., embed=True)) -> bool:
    db = SessionLocal()
    try:
        # Check if user exists and is logged in
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_logged_in:
            raise HTTPException(status_code=403, detail="User is not registered or not logged in")
        
        # Check if cart is not empty
        if not cart_items:
            raise HTTPException(status_code=400, detail="Shopping cart is empty")
        
        # Mark books as rented
        for item in cart_items:
            book_title = item.get("title")
            book = db.query(Book).filter(Book.title == book_title).first()
            if book:
                book.is_rented = True
        
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()