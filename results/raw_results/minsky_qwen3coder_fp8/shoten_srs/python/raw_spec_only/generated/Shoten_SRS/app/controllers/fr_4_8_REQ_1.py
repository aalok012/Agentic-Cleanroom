from fastapi import APIRouter, Body, HTTPException, status
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal


class PrintRequest(Base):
    __tablename__ = "print_requests"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    print_shop_id = Column(Integer, nullable=False)
    status = Column(String, default="pending")


router = APIRouter()


def fr_4_8_REQ_1(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Validate that user is logged in (this would typically be handled by auth middleware)
        # For now, we assume the request contains user info
        if "user_id" not in request or "print_shop_id" not in request:
            raise HTTPException(status_code=400, detail="Missing required fields: user_id or print_shop_id")
        
        # Create a new print request
        new_request = PrintRequest(
            user_id=request["user_id"],
            print_shop_id=request["print_shop_id"]
        )
        
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        
        return {}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()