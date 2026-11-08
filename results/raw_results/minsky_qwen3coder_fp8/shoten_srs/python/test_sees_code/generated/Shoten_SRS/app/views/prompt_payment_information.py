from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.models.store_user_information import User
    # Other user fields would be here

class RentalProcess(Base):
    __tablename__ = "rental_processes"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    completed = Column(Boolean, default=False)
    # Other rental process fields would be here

class DeliveryInfo(Base):
    __tablename__ = "delivery_info"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    completed = Column(Boolean, default=False)
    # Other delivery info fields would be here

router = APIRouter()


def prompt_payment_information(user_id: str) -> dict[str, str]:
    """
    The system displays a form or interface requesting the user to provide payment details such as credit card number or other payment method.

    Args:
        user_id: Unique identifier of the registered and logged-in user who has completed rental and delivery details

    Returns:
        A dictionary containing the prompt message and form fields for payment information input

    Raises:
        HTTPException: If the precondition is violated (The user has completed the rental period selection and delivery information entry, and the system has verified all necessary details).

    Notes:
        Precondition: The user has completed the rental period selection and delivery information entry, and the system has verified all necessary details
        Postcondition: The system awaits the user's payment information to finalize the transaction
        Prerequisite: initiate_rental_process (req 4.6.REQ-1) must have run first.
    """
    db = SessionLocal()
    try:
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if rental process is completed
        rental_process = db.query(RentalProcess).filter(RentalProcess.user_id == user_id).first()
        if not rental_process or not rental_process.completed:
            raise HTTPException(status_code=400, detail="Rental process not completed")

        # Check if delivery info is completed
        delivery_info = db.query(DeliveryInfo).filter(DeliveryInfo.user_id == user_id).first()
        if not delivery_info or not delivery_info.completed:
            raise HTTPException(status_code=400, detail="Delivery information not completed")

        # All preconditions met
        return {
            "prompt": "Please enter your payment information",
            "form_fields": ["card_number", "expiry_date", "cvv"]
        }
    finally:
        db.close()