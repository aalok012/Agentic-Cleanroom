from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.models.store_user_information import User

router = APIRouter()

@router.post("")
def collect_user_information(
    name: str = Body(..., embed=True),
    user_type: str = Body(..., embed=True),
    roll_number: str = Body(..., embed=True),
    shop_id: str = Body(..., embed=True),
    mobile_number: str = Body(..., embed=True),
    email_id: str = Body(..., embed=True)
) -> dict[str, str]:
    # Precondition check
    if not name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    # Validate user_type
    if user_type not in ["student", "bookstore", "general"]:
        raise HTTPException(status_code=400, detail="Invalid user type")
    
    # Validate roll_number for students
    if user_type == "student" and not roll_number:
        raise HTTPException(status_code=400, detail="Roll number is required for students")
    
    # Validate shop_id for bookstores
    if user_type == "bookstore" and not shop_id:
        raise HTTPException(status_code=400, detail="Shop ID is required for bookstores")
    
    # Validate mobile number
    if not mobile_number:
        raise HTTPException(status_code=400, detail="Mobile number is required")
    
    # Validate email
    if not email_id:
        raise HTTPException(status_code=400, detail="Email ID is required")
    
    # Simulate saving to database
    db = SessionLocal()
    try:
        # In a real implementation, we would save the user here
        # For now, we just simulate successful processing
        pass
    finally:
        db.close()
    
    return {"status": "information collected"}
