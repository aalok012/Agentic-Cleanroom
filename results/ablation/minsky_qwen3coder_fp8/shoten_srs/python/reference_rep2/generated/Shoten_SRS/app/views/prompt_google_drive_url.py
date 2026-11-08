from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class PrintJob(Base):
    __tablename__ = "print_jobs"
    __table_args__ = {"extend_existing": True}
    id = Column(String, primary_key=True)
    user_id = Column(String)
    print_shop_id = Column(String)
    google_drive_url = Column(String, nullable=True)

router = APIRouter()

@router.post("")
def prompt_google_drive_url(print_job_id: str = Body(..., embed=True)) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if the print job exists
        print_job = db.query(PrintJob).filter(PrintJob.id == print_job_id).first()
        if not print_job:
            raise HTTPException(status_code=404, detail="Print job not found")
        
        # Check precondition: user has initiated a print request and is in the process of providing document details
        # We assume that if the print job exists, it means the user has initiated a print request
        # and is in the process of providing document details
        
        return {"prompt": "Please enter the Google Drive link URL of the document to be printed"}
    finally:
        db.close()