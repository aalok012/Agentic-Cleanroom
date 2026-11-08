from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.models.store_user_information import User

router = APIRouter()

@router.post("")
def initiate_book_addition(user_id: str = Body(..., embed=True), user_type: str = Body(..., embed=True)) -> bool:
    db = SessionLocal()
    try:
        # Check if user exists and is of valid type
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user.type not in ["bookstore", "printing_store"]:
            raise HTTPException(status_code=403, detail="User type not authorized")
        
        # If we reach here, the user is authorized
        return True
    finally:
        db.close()