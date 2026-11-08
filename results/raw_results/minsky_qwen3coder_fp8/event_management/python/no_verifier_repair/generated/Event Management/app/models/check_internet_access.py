from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal

class InternetAccessModel(Base):
    __tablename__ = "internet_access"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    is_accessible = Column(Boolean, default=False)


def check_internet_access() -> bool:
    """
    The feature is accessible.

    Returns:
        True if internet is accessible, False otherwise

    Raises:
        HTTPException: If the precondition is violated (The system has access to the internet).

    Notes:
        Precondition: The system has access to the internet
        Postcondition: The feature's accessibility is contingent upon the internet being available
        canonical call (must work): {}
        must return on success: true
        error_mode: raise
    """
    db = SessionLocal()
    try:
        # Check if there's a record indicating internet access
        access_record = db.query(InternetAccessModel).first()
        if access_record and access_record.is_accessible:
            return True
        else:
            # Raise exception if internet is not accessible
            raise HTTPException(status_code=400, detail="The system has access to the internet.")
    finally:
        db.close()