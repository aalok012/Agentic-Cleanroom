from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.models.store_user_information import User
    # Other user fields would be here

class RentalProcess(Base):
    __tablename__ = "rental_processes"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    completed = Column(Boolean, default=False)
    # Other rental process fields would be here

class PaymentInformation(Base):
    __tablename__ = "payment_information"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    card_number = Column(String)
    expiry_date = Column(String)
    cvv = Column(String)
    # Other payment fields would be here

router = APIRouter()

@router.post("")
def prompt_payment_information(user_id: str = Body(..., embed=True)) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if the user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if the rental process is completed
        rental_process = db.query(RentalProcess).filter(RentalProcess.user_id == user_id).first()
        if not rental_process or not rental_process.completed:
            raise HTTPException(status_code=400, detail="Rental process not completed")
        
        # Return the payment form
        return {
            "form": "payment_form",
            "fields": ["card_number", "expiry_date", "cvv"]
        }
    finally:
        db.close()