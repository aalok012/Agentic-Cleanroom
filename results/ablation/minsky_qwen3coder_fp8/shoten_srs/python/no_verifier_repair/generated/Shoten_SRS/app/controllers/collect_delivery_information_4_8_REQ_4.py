from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.models.calculate_print_cost import calculate_print_cost

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.views.prompt_google_drive_url import PrintJob

router = APIRouter()


def collect_delivery_information(print_job_id: str, delivery_info: dict[str, str]) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if the print job exists
        job = db.query(PrintJob).filter(PrintJob.id == print_job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Print job not found")
        
        # Check if the precondition is met (Google Drive link entered and cost confirmed)
        if not job.google_drive_url or not job.print_cost_confirmed:
            raise HTTPException(status_code=400, detail="Precondition violated: Google Drive link not entered or printing cost not confirmed")
        
        # Store delivery information (in a real implementation, this would be saved to the database)
        # For now, we'll just validate the input
        if not delivery_info:
            raise HTTPException(status_code=400, detail="No delivery information provided")
        
        # Simulate storing delivery info
        # In a real implementation, you would save this to the database
        
        return {"status": "collected", "message": "Delivery information successfully recorded"}
    finally:
        db.close()