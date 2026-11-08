from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class SelectedOperation(Base):
    __tablename__ = "selected_operations"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    operation_name = Column(String, nullable=False)

router = APIRouter()


def get_operation_details(operation_name: str) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if an operation was previously selected
        selected_op = db.query(SelectedOperation).first()
        if not selected_op:
            raise HTTPException(status_code=400, detail="No operation has been previously selected.")
        
        # Validate that the requested operation matches the selected one
        if selected_op.operation_name != operation_name:
            raise HTTPException(status_code=400, detail="The requested operation does not match the previously selected operation.")
        
        # Return the usage details
        return {
            "operation": operation_name,
            "usage": "Send a POST request with dish names and quantities"
        }
    finally:
        db.close()