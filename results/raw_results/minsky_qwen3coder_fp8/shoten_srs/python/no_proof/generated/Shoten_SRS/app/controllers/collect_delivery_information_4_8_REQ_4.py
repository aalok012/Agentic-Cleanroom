from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.views.prompt_google_drive_url import PrintJob

class DeliveryInfo(Base):
    __tablename__ = "delivery_info"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    print_job_id = Column(String, index=True)
    address = Column(String)
    city = Column(String)
    zip_code = Column(String)

router = APIRouter()

@router.post("")
def collect_delivery_information(
    print_job_id: str = Body(..., embed=True),
    delivery_info: dict[str, str] = Body(..., embed=True)
) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if the print job exists and has been processed
        job = db.query(PrintJob).filter(PrintJob.id == print_job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Print job not found")
        
        # Check if the Google Drive link and printing cost have been confirmed
        if not job.google_drive_url or not job.printing_cost_confirmed:
            raise HTTPException(status_code=400, detail="Precondition violated: Google Drive link and printing cost confirmation required")
        
        # Validate that delivery_info is not empty
        if not delivery_info:
            raise HTTPException(status_code=400, detail="Precondition violated: Delivery information is required")
        
        # Create new delivery info entry
        new_delivery_info = DeliveryInfo(
            print_job_id=print_job_id,
            address=delivery_info.get("address", ""),
            city=delivery_info.get("city", ""),
            zip_code=delivery_info.get("zip_code", "")
        )
        
        db.add(new_delivery_info)
        db.commit()
        db.refresh(new_delivery_info)
        
        return {"status": "collected", "message": "Delivery information successfully recorded"}
    finally:
        db.close()