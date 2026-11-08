from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class SoftCopyPrintCost(Base):
    __tablename__ = "soft_copy_print_costs"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    cost = Column(Float, nullable=False)

router = APIRouter()


def fr_4_8_REQ_3(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Fetch the total cost of printing the soft copy
        soft_copy_cost = db.query(SoftCopyPrintCost.cost).first()
        
        if soft_copy_cost is None:
            raise HTTPException(status_code=404, detail="Soft copy print cost not found.")
        
        return {}
    finally:
        db.close()