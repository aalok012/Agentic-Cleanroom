from fastapi import APIRouter, Body, HTTPException
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.controllers.validate_and_store_book_details import Book

type BookModel = Book

router = APIRouter()


def store_payment_details(payment_info: dict, user_id: str) -> bool:
    """
    The system accepts the payment details and stores them securely for future transactions.

    Args:
        payment_info: Dictionary containing payment acceptance details like bank account number, IFSC Code etc.
        user_id: Unique identifier of the user, bookstore, or printing store

    Returns:
        True if the payment details were stored successfully

    Raises:
        HTTPException: If the precondition is violated (The user has completed the book details entry and is now entering payment information).
    """
    db = SessionLocal()
    try:
        # Check if the user has initiated book addition (prerequisite)
        book = db.query(Book).filter(Book.user_id == user_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="User has not initiated book addition.")

        # Validate payment info
        if not payment_info.get("bank_account_number") or not payment_info.get("ifsc_code"):
            raise HTTPException(status_code=400, detail="Payment details are incomplete.")

        # Update the book record with payment details
        book.bank_account_number = payment_info["bank_account_number"]
        book.ifsc_code = payment_info["ifsc_code"]
        
        db.commit()
        return True
    finally:
        db.close()