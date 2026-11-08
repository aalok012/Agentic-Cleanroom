from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.views.prompt_google_drive_url import PrintJob

router = APIRouter()

@router.post("")
def prompt_payment_information(print_job_id: str = Body(..., embed=True)) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if the print job exists
        job = db.query(PrintJob).filter(PrintJob.id == print_job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Print job not found")
        
        # Check preconditions
        if not job.document_uploaded:
            raise HTTPException(status_code=400, detail="Document upload not completed")
        if not job.cost_confirmed:
            raise HTTPException(status_code=400, detail="Cost confirmation not completed")
        if not job.delivery_info_entered:
            raise HTTPException(status_code=400, detail="Delivery information not entered")
        
        # All preconditions met, return the prompt
        return {"prompt": "Please enter your payment information to complete the transaction"}
    finally:
        db.close()