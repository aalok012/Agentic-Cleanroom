from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.models._stubs import Rental
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.models.store_user_information import User

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.controllers.validate_and_store_book_details import Book

router = APIRouter()


def display_rented_books(user_id: str) -> list[dict[str, str]]:
    """
    The system presents a list of rented books including their titles, prices, and quantities.

    Args:
        user_id: Unique identifier of the registered and logged-in user whose transaction was successful

    Returns:
        A list of dictionaries representing rented books with their titles, prices, and quantities

    Raises:
        HTTPException: If the precondition is violated (The user has successfully completed the payment process and the transaction is finalized).
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    db = SessionLocal()
    try:
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get rented books for the user
        rentals = db.query(Rental).filter(Rental.user_id == user_id).all()
        if not rentals:
            return []

        books = []
        for rental in rentals:
            book = db.query(Book).filter(Book.id == rental.book_id).first()
            if book:
                books.append({
                    "title": book.title,
                    "price": book.price,
                    "quantity": rental.quantity
                })
        return books
    finally:
        db.close()