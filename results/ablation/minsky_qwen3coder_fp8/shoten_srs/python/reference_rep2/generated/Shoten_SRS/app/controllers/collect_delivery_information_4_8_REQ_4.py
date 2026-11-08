from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.views.prompt_google_drive_url import PrintJob

class DeliveryInfoModel(Base):
    __tablename__ = "delivery_info"
    __table_args__ = {"extend_existing": True}
    user_id = Column(String)
    street = Column(String)
    city = Column(String)
    zip_code = Column(String)
    id = Column(Integer, primary_key=True)
    print_job_id = Column(String, index=True)
    zip = Column(String)

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
        
        # Check if the required fields are present in delivery_info
        required_fields = ["street", "city", "zip"]
        for field in required_fields:
            if field not in delivery_info or not delivery_info[field]:
                raise HTTPException(status_code=400, detail="Missing required delivery information")
        
        # Check if the print cost has been calculated (prerequisite)
        if not job.print_cost_calculated:
            raise HTTPException(status_code=400, detail="Print cost has not been calculated yet")
        
        # Create and save delivery info
        new_delivery_info = DeliveryInfoModel(
            print_job_id=print_job_id,
            street=delivery_info["street"],
            city=delivery_info["city"],
            zip=delivery_info["zip"]
        )
        db.add(new_delivery_info)
        db.commit()
        db.refresh(new_delivery_info)
        
        return {"status": "collected", "message": "Delivery information successfully recorded"}
    finally:
        db.close()