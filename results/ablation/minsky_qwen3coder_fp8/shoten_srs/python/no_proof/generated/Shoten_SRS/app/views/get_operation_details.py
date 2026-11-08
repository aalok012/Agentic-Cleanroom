from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class SelectedOperation(Base):
    __tablename__ = "selected_operations"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    operation_name = Column(String, nullable=False)

router = APIRouter()


def get_operation_details(operation_name: str) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if the operation was previously selected
        selected_op = db.query(SelectedOperation).filter_by(operation_name=operation_name).first()
        if not selected_op:
            raise HTTPException(status_code=404, detail="Operation not previously selected")
        
        # Return detailed usage information
        return {
            "operation": operation_name,
            "details": "Display help overview"
        }
    finally:
        db.close()