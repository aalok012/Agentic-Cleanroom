from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.views.prompt_google_drive_url import PrintJob

router = APIRouter()


def calculate_print_cost(google_drive_url: str) -> dict[str, float]:
    db = SessionLocal()
    try:
        # Validate the Google Drive URL
        if not google_drive_url or "drive.google.com" not in google_drive_url:
            raise HTTPException(status_code=400, detail="Invalid Google Drive URL")
        
        # Check if the print job exists in the database
        print_job = db.query(PrintJob).filter(PrintJob.google_drive_url == google_drive_url).first()
        
        if not print_job:
            raise HTTPException(status_code=404, detail="Print job not found")
        
        # Return the total cost
        return {"total_cost": print_job.total_cost}
    finally:
        db.close()