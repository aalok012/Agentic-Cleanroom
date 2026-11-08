from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.views.prompt_google_drive_url import PrintJob

router = APIRouter()

def calculate_print_cost(google_drive_url: str) -> dict[str, float]:
    db = SessionLocal()
    try:
        # Validate the Google Drive URL
        if not google_drive_url or "drive.google.com" not in google_drive_url:
            raise HTTPException(status_code=400, detail="Invalid Google Drive URL")
        
        # Fetch the print job from the database
        print_job = db.query(PrintJob).filter(PrintJob.google_drive_url == google_drive_url).first()
        
        # If no print job found, raise an exception
        if not print_job:
            raise HTTPException(status_code=404, detail="Print job not found")
        
        # Return the total cost from the database
        return {"total_cost": print_job.total_cost}
    finally:
        db.close()