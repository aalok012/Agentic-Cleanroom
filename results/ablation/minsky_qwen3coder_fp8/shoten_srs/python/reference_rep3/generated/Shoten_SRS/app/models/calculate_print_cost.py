from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.views.prompt_google_drive_url import PrintJob

router = APIRouter()


def calculate_print_cost(google_drive_url: str) -> dict[str, float]:
    db = SessionLocal()
    try:
        # Validate the Google Drive URL
        if not google_drive_url or "drive.google.com" not in google_drive_url:
            raise HTTPException(status_code=400, detail="Invalid Google Drive URL")
        
        # In a real implementation, we would fetch the print job from the database
        # and calculate the cost based on the document size, number of pages, etc.
        # For now, we'll simulate the calculation.
        
        # Simulate cost calculation (this would come from actual logic)
        total_cost = 12.5
        
        # Save the calculated cost back to the database (if needed)
        # print_job = db.query(PrintJob).filter(PrintJob.google_drive_url == google_drive_url).first()
        # if print_job:
        #     print_job.total_cost = total_cost
        #     db.commit()
        
        return {"total_cost": total_cost}
    finally:
        db.close()