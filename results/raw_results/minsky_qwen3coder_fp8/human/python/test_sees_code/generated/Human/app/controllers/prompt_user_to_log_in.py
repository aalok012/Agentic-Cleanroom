from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.human.python.test_sees_code.generated.Human.app.extensions import Base, SessionLocal

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    is_logged_in = Column(Boolean, default=False)

router = APIRouter()


def prompt_user_to_log_in() -> dict[str, str]:
    """System prompts the user to log in before proceeding with event registration."""
    db = SessionLocal()
    try:
        # Check if user is logged in
        user = db.query(User).filter(User.is_logged_in == True).first()
        if user is None:
            raise HTTPException(status_code=403, detail="Please log in to register for the event.")
        
        # If user is logged in, return success message
        return {"message": "Please log in to register for the event."}
    finally:
        db.close()