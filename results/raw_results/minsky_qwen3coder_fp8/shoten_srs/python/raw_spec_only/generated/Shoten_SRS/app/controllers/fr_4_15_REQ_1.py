from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal


class OperationOverview(Base):
    __tablename__ = "operation_overview"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    description = Column(String(255))


router = APIRouter()


def fr_4_15_REQ_1(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Fetch the overview information from the database
        overview = db.query(OperationOverview).first()
        if not overview:
            raise HTTPException(status_code=404, detail="Overview not found")
        
        # Return the overview information
        return {
            "description": overview.description
        }
    finally:
        db.close()