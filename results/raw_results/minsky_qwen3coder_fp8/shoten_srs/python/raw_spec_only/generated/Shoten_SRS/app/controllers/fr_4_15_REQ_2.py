from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal


class Operation(Base):
    __tablename__ = "operations"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


router = APIRouter()


def fr_4_15_REQ_2(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Extract operation name from request
        operation_name = request.get("operation_name")
        if not operation_name:
            raise HTTPException(status_code=400, detail="Operation name is required.")
        
        # Check if operation exists
        operation = db.query(Operation).filter(Operation.name == operation_name).first()
        if not operation:
            raise HTTPException(status_code=404, detail="Operation not found.")
        
        # Return success response
        return {}
    finally:
        db.close()