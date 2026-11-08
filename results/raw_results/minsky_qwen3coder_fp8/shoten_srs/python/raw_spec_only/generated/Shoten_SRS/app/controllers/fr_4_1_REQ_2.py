from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    institute_roll_number = Column(String)
    shop_id = Column(String)
    mobile_number = Column(String, nullable=False)
    email_id = Column(String, nullable=False)


router = APIRouter()


def fr_4_1_REQ_2(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Validate required fields
        if "name" not in request or not request["name"]:
            raise HTTPException(status_code=400, detail="Name is required")
        
        if "mobile_number" not in request or not request["mobile_number"]:
            raise HTTPException(status_code=400, detail="Mobile Number is required")
        
        if "email_id" not in request or not request["email_id"]:
            raise HTTPException(status_code=400, detail="Email ID is required")
        
        # Check if it's a student or bookstore
        is_student = "institute_roll_number" in request and request["institute_roll_number"]
        is_bookstore = "shop_id" in request and request["shop_id"]
        
        # Validate that only one of the optional fields is provided
        if is_student and is_bookstore:
            raise HTTPException(status_code=400, detail="Cannot specify both Institute Roll Number and Shop ID")
        
        # Create user instance
        user = User(
            name=request["name"],
            institute_roll_number=request.get("institute_roll_number"),
            shop_id=request.get("shop_id"),
            mobile_number=request["mobile_number"],
            email_id=request["email_id"]
        )
        
        # Save to database
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return {}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()