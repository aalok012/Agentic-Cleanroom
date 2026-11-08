from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.models.store_user_information import User

router = APIRouter()

@router.post("")
def change_password(
    user_id: str = Body(..., embed=True),
    old_password: str = Body(..., embed=True),
    new_password: str = Body(..., embed=True),
    confirm_new_password: str = Body(..., embed=True)
) -> bool:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user.password != old_password:
            raise HTTPException(status_code=400, detail="Old password is incorrect")
        
        if new_password != confirm_new_password:
            raise HTTPException(status_code=400, detail="New passwords do not match")
        
        user.password = new_password
        db.commit()
        return True
    finally:
        db.close()