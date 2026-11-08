from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal


class InternetAccess(Base):
    __tablename__ = "internet_access"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    enabled = Column(Boolean, default=True)


router = APIRouter()


def fr_3_2_REQ_1(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Check if internet access is enabled
        access_record = db.query(InternetAccess).first()
        if not access_record or not access_record.enabled:
            raise HTTPException(status_code=403, detail="Internet access is not enabled.")
        
        # If we reach here, internet access is enabled
        return {}
    finally:
        db.close()