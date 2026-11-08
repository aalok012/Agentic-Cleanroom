from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    institute_roll_number = Column(String)
    shop_id = Column(String)
    mobile_number = Column(String, nullable=False)
    email_id = Column(String, nullable=False)

router = APIRouter()

@router.post("")
def store_user_information(
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    name: str = Body(..., embed=True),
    institute_roll_number: str = Body(..., embed=True),
    shop_id: str = Body(..., embed=True),
    mobile_number: str = Body(..., embed=True),
    email_id: str = Body(..., embed=True)
) -> bool:
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Create new user
        new_user = User(
            username=username,
            password=password,
            name=name,
            institute_roll_number=institute_roll_number,
            shop_id=shop_id,
            mobile_number=mobile_number,
            email_id=email_id
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()