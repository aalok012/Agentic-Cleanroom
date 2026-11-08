from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal

class Stakeholder(Base):
    __tablename__ = "stakeholders"
    __table_args__ = {"extend_existing": True}
    
    stakeholder_id = Column(String, primary_key=True)
    login_credentials = Column(String)
    personal_details = Column(String)

router = APIRouter()

@router.post("")
def get_stakeholder_info(stakeholder_id: str = Body(..., embed=True)) -> dict[str, str]:
    if not stakeholder_id:
        raise HTTPException(status_code=400, detail="Stakeholder ID cannot be empty")
    
    db = SessionLocal()
    try:
        stakeholder = db.query(Stakeholder).filter(Stakeholder.stakeholder_id == stakeholder_id).first()
        if not stakeholder:
            raise HTTPException(status_code=404, detail="Stakeholder not found")
        
        return {
            "login_credentials": stakeholder.login_credentials,
            "personal_details": stakeholder.personal_details
        }
    finally:
        db.close()