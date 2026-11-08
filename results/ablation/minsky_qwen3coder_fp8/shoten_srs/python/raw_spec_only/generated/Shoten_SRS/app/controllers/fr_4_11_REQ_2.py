from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_1_REQ_2 import User

router = APIRouter()

@router.post("")
def fr_4_11_REQ_2(request: dict = Body(..., embed=True)) -> dict:
    db = SessionLocal()
    try:
        # Fetch the user (assuming there's a way to identify the user, e.g., from auth)
        # For simplicity, we'll assume a single user exists with id=1
        user = db.query(User).filter(User.id == 1).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update fields if provided in request
        if "name" in request:
            user.name = request["name"]
        if "mailing_address" in request:
            user.mailing_address = request["mailing_address"]
        if "billing_address" in request:
            user.billing_address = request["billing_address"]
        if "payment_info" in request:
            user.payment_info = request["payment_info"]
        
        db.commit()
        db.refresh(user)
        return {}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()