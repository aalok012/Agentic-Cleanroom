from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.controllers.initiate_rental_process import Rental

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.models.save_delivery_information import DeliveryInformation

router = APIRouter()

@router.post("")
def collect_delivery_information(user_id: str = Body(..., embed=True), delivery_details: dict[str, str] = Body(..., embed=True)) -> bool:
    db = SessionLocal()
    try:
        # Check if the user has initiated the rental process
        rental = db.query(Rental).filter(Rental.user_id == user_id).first()
        if not rental:
            raise HTTPException(status_code=400, detail="User has not initiated rental process")
        
        # Check if rental period is entered and rent charges are calculated
        if not rental.rental_period or not rental.rent_charges:
            raise HTTPException(status_code=400, detail="User has not entered the rental period and the system has not calculated the rent charges")
        
        # Create new delivery information entry
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