from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class RentedBook(Base):
    __tablename__ = "rented_books"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

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
        raise HTTPException(status_code=400, detail="User ID cannot be empty")

    db = SessionLocal()
    try:
        rented_books = (
            db.query(RentedBook)
            .filter(RentedBook.user_id == user_id)
            .all()
        )

        result = [
            {
                "title": book.title,
                "price": book.price,
                "quantity": book.quantity
            }
            for book in rented_books
        ]

        return result
    finally:
        db.close()