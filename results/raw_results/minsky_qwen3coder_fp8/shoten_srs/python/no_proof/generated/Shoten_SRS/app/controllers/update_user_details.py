from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.models.store_user_information import User

router = APIRouter()

@router.post("")
def update_user_details(user_id: str = Body(..., embed=True), name: str = Body(..., embed=True), mailing_address: str = Body(..., embed=True), billing_address: str = Body(..., embed=True), payment_info: dict = Body(..., embed=True)) -> bool:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Validate inputs
        if not name or not mailing_address or not billing_address or not payment_info:
            raise HTTPException(status_code=400, detail="All fields are required")
        
        # Update user details
        user.name = name
        user.mailing_address = mailing_address
        user.billing_address = billing_address
        user.payment_info = str(payment_info)
        
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()