from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class PrintJob(Base):
    __tablename__ = "print_jobs"
    __table_args__ = {"extend_existing": True}
    id = Column(String, primary_key=True)
    user_id = Column(String)
    print_shop_id = Column(String)
    google_drive_link = Column(String, nullable=True)

router = APIRouter()

@router.post("")
def prompt_google_drive_url(print_job_id: str = Body(..., embed=True)) -> dict[str, str]:
    if not print_job_id:
        raise HTTPException(status_code=400, detail="Print job ID cannot be empty")
    
    db = SessionLocal()
    try:
        # Check if the print job exists
        print_job = db.query(PrintJob).filter(PrintJob.id == print_job_id).first()
        if not print_job:
            raise HTTPException(status_code=404, detail="Print job not found")
        
        # Check if the print job is in the correct state (initiated but no link provided)
        if print_job.google_drive_link is not None:
            raise HTTPException(status_code=400, detail="Google Drive link already provided")
        
        # Return the prompt message
        return {"prompt": "Please enter the Google Drive link URL of the document to be printed"}
    finally:
        db.close()