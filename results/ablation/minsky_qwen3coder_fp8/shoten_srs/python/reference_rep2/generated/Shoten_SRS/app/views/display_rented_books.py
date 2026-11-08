from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.models.store_user_information import User
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.controllers.calculate_and_display_rent import Rental
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.controllers.validate_and_store_book_details import Book

class RentalBook(Base):
    __tablename__ = "rental_books"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    rental_id = Column(Integer, nullable=False)
    book_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

router = APIRouter()

def display_rented_books(user_id: str) -> list[dict[str, str]]:
    """
    The system presents a list of rented books including their titles, prices, and quantities.

    Args:
        user_id: Unique identifier of the registered and logged-in user

    Returns:
        List of rented books including their titles, prices, and quantities

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

        # Get rentals associated with the user
        rentals = db.query(Rental).filter(Rental.user_id == user_id).all()
        if not rentals:
            return []

        rented_books = []
        for rental in rentals:
            # Get rental books for each rental
            rental_books = db.query(RentalBook).filter(RentalBook.rental_id == rental.id).all()
            for rb in rental_books:
                # Get book details
                book = db.query(Book).filter(Book.id == rb.book_id).first()
                if book:
                    rented_books.append({
                        "title": book.title,
                        "price": book.price,
                        "quantity": rb.quantity
                    })
        
        return rented_books
    finally:
        db.close()