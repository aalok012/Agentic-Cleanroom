from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal

router = APIRouter()

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.views.get_help_overview import Operation

@router.post("")
def select_help_operation(operation_name: str = Body(..., embed=True)) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if the operation exists
        operation = db.query(Operation).filter(Operation.name == operation_name).first()
        if not operation:
            raise HTTPException(status_code=404, detail="Operation not found")
        
        # Return acknowledgment
        return {"status": "success", "selected_operation": operation_name}
    finally:
        db.close()