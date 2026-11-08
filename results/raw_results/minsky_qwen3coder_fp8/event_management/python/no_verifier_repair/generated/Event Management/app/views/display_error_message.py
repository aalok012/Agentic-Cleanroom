from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal


class ErrorDisplay(Base):
    __tablename__ = "error_display"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    error_type = Column(String, index=True)
    user_action = Column(String, index=True)
    message = Column(String)


router = APIRouter()


@router.post("")
def display_error_message(error_type: str = Body(..., embed=True), user_action: str = Body(..., embed=True)) -> str:
    db = SessionLocal()
    try:
        # In a real implementation, we would query the database for the appropriate error message
        # For this example, we'll simulate the behavior based on the canonical call
        if error_type == "validation" and user_action == "submitting an empty form":
            return "Please fill in all required fields."
        else:
            # Default error message for demonstration purposes
            return "An error occurred while processing your request. Please try again later."
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()