from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.controllers.initiate_book_addition import initiate_book_addition

class BookAdditionRecord(Base):
    __tablename__ = "book_addition_records"
    __table_args__ = {"extend_existing": True}
    user_id = Column(String, primary_key=True)
    user_type = Column(String)
    book_details_completed = Column(Boolean, default=False)

router = APIRouter()

@router.post("")
def store_payment_details(payment_info: dict = Body(..., embed=True)) -> dict:
    db = SessionLocal()
    try:
        # Check if the user has completed book details entry
        record = db.query(BookAdditionRecord).filter(BookAdditionRecord.user_id == payment_info.get("user_id")).first()
        if not record or not record.book_details_completed:
            # Call the prerequisite function to ensure book details are completed
            initiate_book_addition(user_id=payment_info.get("user_id"), user_type=payment_info.get("user_type"))
            
            # After calling initiate_book_addition, check again
            record = db.query(BookAdditionRecord).filter(BookAdditionRecord.user_id == payment_info.get("user_id")).first()
            if not record or not record.book_details_completed:
                raise HTTPException(status_code=400, detail="Precondition violated: User has not completed book details entry")
        
        # Validate payment info
        if not payment_info.get("bank_account_number") or not payment_info.get("ifsc_code"):
            raise HTTPException(status_code=400, detail="Invalid payment details: Bank account number and IFSC code are required")
        
        # In a real implementation, we would store the payment details securely here
        # For now, we'll just simulate storing them
        
        return {"status": "success", "message": "Payment details stored successfully"}
    finally:
        db.close()