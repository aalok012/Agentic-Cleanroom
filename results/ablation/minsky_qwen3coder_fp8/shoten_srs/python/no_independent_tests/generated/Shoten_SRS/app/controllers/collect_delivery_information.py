from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.models.store_user_information import User

router = APIRouter()

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.models.save_delivery_information import DeliveryInformation


def collect_delivery_information(user_id: str, delivery_details: dict[str, str]) -> bool:
    db = SessionLocal()
    try:
        # Check if user has initiated rental process (precondition)
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if rental period is entered and rent charges are calculated
        # This is a simplified check - in reality, you'd need to verify
        # that the rental process was initiated and completed
        if not user.rental_period_entered or not user.rent_charges_calculated:
            raise HTTPException(status_code=400, detail="Precondition violated: Rental period not entered or rent charges not calculated")
        
        # Save delivery information
        delivery_info = DeliveryInformation(
            user_id=user_id,
            address=delivery_details.get("address", ""),
            contact=delivery_details.get("contact", "")
        )
        db.add(delivery_info)
        db.commit()
        db.refresh(delivery_info)
        
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()