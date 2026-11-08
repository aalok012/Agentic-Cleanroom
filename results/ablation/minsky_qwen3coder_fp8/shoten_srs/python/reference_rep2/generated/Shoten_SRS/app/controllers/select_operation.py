from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.views.get_help_overview import Operation

router = APIRouter()

@router.post("")
def select_operation(operation_name: str = Body(..., embed=True)) -> dict[str, str]:
    db = SessionLocal()
    try:
        operation = db.query(Operation).filter(Operation.name == operation_name).first()
        if not operation:
            raise HTTPException(status_code=404, detail="Operation not found")
        
        # System prepares to display detailed information for the selected operation
        return {"status": "selected", "operation": operation.name}
    finally:
        db.close()