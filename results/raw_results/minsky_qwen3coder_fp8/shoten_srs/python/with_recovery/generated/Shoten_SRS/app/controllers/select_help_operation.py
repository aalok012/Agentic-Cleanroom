from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.views.get_help_overview import Operation

router = APIRouter()


def select_help_operation(operation_name: str) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if the operation exists in the database
        operation = db.query(Operation).filter(Operation.name == operation_name).first()
        if not operation:
            raise HTTPException(status_code=400, detail="Operation not found")
        
        # Return acknowledgment of the selected operation
        return {"status": "success", "selected_operation": operation_name}
    finally:
        db.close()