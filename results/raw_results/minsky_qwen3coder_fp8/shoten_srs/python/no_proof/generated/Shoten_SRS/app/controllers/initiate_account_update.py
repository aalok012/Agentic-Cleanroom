from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.models.store_user_information import User

router = APIRouter()

@router.post("")
def initiate_account_update(user_id: str = Body(..., embed=True), update_data: dict = Body(..., embed=True)) -> None:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update user attributes based on update_data
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise HTTPException(status_code=400, detail=f"Invalid field '{key}' for user update")
        
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()