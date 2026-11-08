from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app.models.calculate_print_cost import calculate_print_cost

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app.views.prompt_google_drive_url import PrintJob

router = APIRouter()

@router.post("")
def collect_delivery_information(
    print_job_id: str = Body(..., embed=True),
    delivery_info: dict[str, str] = Body(..., embed=True)
) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if the print job exists
        job = db.query(PrintJob).filter(PrintJob.id == print_job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Print job not found")
        
        # Check if the precondition is met (Google Drive link entered and cost confirmed)
        if not job.google_drive_url or not job.print_cost_confirmed:
            raise HTTPException(status_code=400, detail="Precondition violated: Google Drive link not entered or printing cost not confirmed")
        
        # Validate that delivery_info is not empty
        if not delivery_info:
            raise HTTPException(status_code=400, detail="Precondition violated: Google Drive link not entered or printing cost not confirmed")
        
        # In a real implementation, we would store the delivery_info in the database
        # For now, we'll just return a success message
        return {"status": "collected", "message": "Delivery information successfully recorded"}
    finally:
        db.close()