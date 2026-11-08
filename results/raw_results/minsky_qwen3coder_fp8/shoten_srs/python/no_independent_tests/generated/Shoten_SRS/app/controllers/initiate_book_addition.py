from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.models.store_user_information import User

router = APIRouter()

@router.post("")
def initiate_book_addition(user_id: str = Body(..., embed=True), user_type: str = Body(..., embed=True)) -> bool:
    db = SessionLocal()
    try:
        # Check if user exists and is logged in
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_logged_in:
            raise HTTPException(status_code=403, detail="User is not registered or not logged in")
        
        # Check if user type is valid
        if user_type not in ["bookstore", "printing_store"]:
            raise HTTPException(status_code=400, detail="Invalid user type")
        
        # Check if user is of correct type
        if user.type != user_type:
            raise HTTPException(status_code=403, detail="User type does not match the provided type")
        
        # If all checks pass, return True
        return True
    finally:
        db.close()