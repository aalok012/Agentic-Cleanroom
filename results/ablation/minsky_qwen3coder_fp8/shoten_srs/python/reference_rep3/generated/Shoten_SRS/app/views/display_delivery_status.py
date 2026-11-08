from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.views.prompt_google_drive_url import PrintJob

router = APIRouter()

@router.post("")
def display_delivery_status(print_job_id: str = Body(..., embed=True)) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if the print job exists and has a valid status
        job = db.query(PrintJob).filter(PrintJob.id == print_job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Print job not found")
        
        # Check if the job has been successfully processed (precondition)
        if not job.status or job.status != "completed":
            raise HTTPException(status_code=400, detail="Precondition violated: User has not successfully completed all steps including payment processing")
        
        # Return the delivery status
        return {
            "status": job.status,
            "tracking_number": job.tracking_number
        }
    finally:
        db.close()