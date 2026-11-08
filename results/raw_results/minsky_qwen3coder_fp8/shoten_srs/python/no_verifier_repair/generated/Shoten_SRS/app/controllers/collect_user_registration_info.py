from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class UserRegistration(Base):
    __tablename__ = "user_registrations"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    institute_roll_number = Column(String, nullable=True)
    shop_id = Column(String, nullable=True)
    mobile_number = Column(String, nullable=False)
    email_id = Column(String, nullable=False)

router = APIRouter()

@router.post("")
def collect_user_registration_info(
    name: str = Body(..., embed=True),
    institute_roll_number: str = Body(..., embed=True),
    shop_id: str = Body(..., embed=True),
    mobile_number: str = Body(..., embed=True),
    email_id: str = Body(..., embed=True)
) -> None:
    db = SessionLocal()
    try:
        # Validate preconditions
        if not name or not mobile_number or not email_id:
            raise HTTPException(status_code=400, detail="Name, mobile number, and email ID are required.")
        
        # Create new user registration entry
        new_user = UserRegistration(
            name=name,
            institute_roll_number=institute_roll_number,
            shop_id=shop_id,
            mobile_number=mobile_number,
            email_id=email_id
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()