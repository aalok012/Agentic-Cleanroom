from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.views.prompt_google_drive_url import PrintJob

router = APIRouter()


def prompt_payment_information(print_job_id: str) -> dict[str, str]:
    """
    The system displays a prompt requesting the user to provide payment details.

    Args:
        print_job_id: Unique identifier of the completed print job requiring payment information

    Returns:
        A prompt message requesting the user to provide payment details

    Raises:
        HTTPException: If the precondition is violated (The user has completed the document upload, cost confirmation, and delivery information entry).
    """
    db = SessionLocal()
    try:
        # Check if the print job exists
        job = db.query(PrintJob).filter(PrintJob.id == print_job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Print job not found")
        
        # Check preconditions
        if not (job.document_uploaded and job.cost_confirmed and job.delivery_info_entered):
            raise HTTPException(
                status_code=400,
                detail="Precondition violated: User has not completed document upload, cost confirmation, and delivery information entry"
            )
        
        return {"prompt": "Please enter your payment information to complete the transaction"}
    finally:
        db.close()