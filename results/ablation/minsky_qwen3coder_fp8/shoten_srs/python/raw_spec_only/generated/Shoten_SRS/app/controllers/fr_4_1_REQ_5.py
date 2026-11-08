from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class Information(Base):
    __tablename__ = "informations"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, nullable=False)

router = APIRouter()

@router.post("")
def fr_4_1_REQ_5(request: dict = Body(..., embed=True)) -> dict:
    db = SessionLocal()
    try:
        info = Information(data=str(request.get("data", "")))
        db.add(info)
        db.commit()
        db.refresh(info)
        return {}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to store information in the database")
    finally:
        db.close()