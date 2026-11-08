from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.extensions import Base, SessionLocal


class UserRegistrationInfo(Base):
    __tablename__ = "user_registration_info"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    institute_roll_number = Column(String, nullable=True)
    shop_id = Column(String, nullable=True)
    mobile_number = Column(String, nullable=False)
    email_id = Column(String, nullable=False)


router = APIRouter()


def collect_user_registration_info(
    name: str = Body(..., embed=True),
    institute_roll_number: str = Body(..., embed=True),
    shop_id: str = Body(..., embed=True),
    mobile_number: str = Body(..., embed=True),
    email_id: str = Body(..., embed=True)
) -> None:
    """
    The system collects the following information from the user: Name, Institute Roll Number (if student), Shop ID (if bookstore), Mobile Number, Email ID.

    Args:
        name: The full name of the user
        institute_roll_number: Institute roll number (applicable only for students)
        shop_id: Shop ID (applicable only for bookstores)
        mobile_number: Mobile number of the user
        email_id: Email ID of the user

    Returns:
        The system collects the following information from the user

    Raises:
        HTTPException: If the precondition is violated (The user has initiated the account creation process).

    Notes:
        Precondition: The user has initiated the account creation process
        Postcondition: The system has received all required information from the user for account creation
    """
    # Check precondition
    if not name or not mobile_number or not email_id:
        raise HTTPException(status_code=400, detail="Name, mobile number, and email ID are required.")
    
    db = SessionLocal()
    try:
        # Create new user registration info entry
        user_info = UserRegistrationInfo(
            name=name,
            institute_roll_number=institute_roll_number,
            shop_id=shop_id,
            mobile_number=mobile_number,
            email_id=email_id
        )
        db.add(user_info)
        db.commit()
        db.refresh(user_info)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save user registration info: {str(e)}")
    finally:
        db.close()