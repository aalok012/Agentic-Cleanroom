from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.controllers.collect_delivery_information_4_8_REQ_4 import DeliveryInfoModel as DeliveryInfo

router = APIRouter()

@router.post("")
def save_delivery_info(user_id: str = Body(..., embed=True), delivery_info: dict[str, str] = Body(..., embed=True)) -> bool:
    db = SessionLocal()
    try:
        # Check if user has initiated the purchase process and is in the delivery information step
        # This is a placeholder check - in reality, this would involve checking the user's current state
        # For now, we'll assume the precondition is met if the user_id exists in some purchase context
        # In a real implementation, this would involve checking a purchase session or user state
        
        # Validate that delivery_info is not empty
        if not delivery_info:
            raise HTTPException(status_code=400, detail="Delivery information cannot be empty")
        
        # Create or update delivery info
        existing_delivery_info = db.query(DeliveryInfo).filter(DeliveryInfo.user_id == user_id).first()
        
        if existing_delivery_info:
            # Update existing record
            for key, value in delivery_info.items():
                if hasattr(existing_delivery_info, key):
                    setattr(existing_delivery_info, key, value)
        else:
            # Create new record
            new_delivery_info = DeliveryInfo(
                user_id=user_id,
                **delivery_info
            )
            db.add(new_delivery_info)
        
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()