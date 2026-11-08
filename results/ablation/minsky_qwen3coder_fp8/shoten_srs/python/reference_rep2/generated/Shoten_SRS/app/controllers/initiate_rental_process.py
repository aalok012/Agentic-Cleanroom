from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal


from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.controllers.validate_and_store_book_details import Book


from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.models.store_user_information import User


router = APIRouter()


@router.post("")
def initiate_rental_process(
    user_id: str = Body(..., embed=True),
    shopping_cart: list[dict[str, str]] = Body(..., embed=True),
) -> bool:
    db = SessionLocal()
    try:
        # Check if user exists and is logged in
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.logged_in:
            raise HTTPException(status_code=403, detail="User is not registered or logged in")

        # Check if shopping cart has at least one book
        if not shopping_cart:
            raise HTTPException(status_code=400, detail="Shopping cart is empty")

        # Mark books as rented
        for item in shopping_cart:
            title = item.get("title")
            book = db.query(Book).filter(Book.title == title).first()
            if book:
                book.rented = True

        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()