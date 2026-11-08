from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal

class ErrorMessage(Base):
    __tablename__ = "error_messages"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    error_type = Column(String)
    user_action = Column(String)
    message = Column(String)

router = APIRouter()

@router.post("")
def display_error_message(error_type: str = Body(..., embed=True), user_action: str = Body(..., embed=True)) -> str:
    db = SessionLocal()
    try:
        # Query the database for an appropriate error message
        error_message = db.query(ErrorMessage).filter(
            ErrorMessage.error_type == error_type,
            ErrorMessage.user_action == user_action
        ).first()
        
        if error_message:
            return error_message.message
        else:
            # Default error message if none found
            return "An unexpected error occurred. Please try again later."
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error retrieving error message")
    finally:
        db.close()