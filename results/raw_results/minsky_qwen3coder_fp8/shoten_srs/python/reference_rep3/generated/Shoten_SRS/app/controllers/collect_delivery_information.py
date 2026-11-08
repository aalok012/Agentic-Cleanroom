from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.controllers.calculate_and_display_rent import Rental

class DeliveryInformation(Base):
    __tablename__ = "delivery_information"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    address = Column(String)
    contact = Column(String)

router = APIRouter()

@router.post("")
def collect_delivery_information(user_id: str = Body(..., embed=True), delivery_details: dict[str, str] = Body(..., embed=True)) -> bool:
    db = SessionLocal()
    try:
        # Check if the user has initiated the rental process
        rental = db.query(Rental).filter(Rental.user_id == user_id).first()
        if not rental:
            raise HTTPException(status_code=404, detail="Rental process not initiated")
        
        # Check if rent charges have been calculated
        if not rental.rent_charges_calculated:
            raise HTTPException(status_code=400, detail="The user has entered the rental period and the system has calculated the rent charges")
        
        # Validate delivery details
        if not delivery_details or not delivery_details.get("address") or not delivery_details.get("contact"):
            raise HTTPException(status_code=400, detail="Delivery details are incomplete")
        
        # Create or update delivery information
        delivery_info = db.query(DeliveryInformation).filter(DeliveryInformation.user_id == user_id).first()
        if not delivery_info:
            delivery_info = DeliveryInformation(user_id=user_id)
            db.add(delivery_info)
        
        delivery_info.address = delivery_details["address"]
        delivery_info.contact = delivery_details["contact"]
        
        db.commit()
        db.refresh(delivery_info)
        
        return True
    finally:
        db.close()