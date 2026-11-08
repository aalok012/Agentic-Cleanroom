from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal


class SellerLocation(Base):
    __tablename__ = "seller_locations"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    type = Column(String)  # "bookstore" or "printing_store"


router = APIRouter()


@router.post("")
def get_seller_locations_map() -> str:
    db = SessionLocal()
    try:
        sellers = db.query(SellerLocation).all()
        if not sellers:
            raise HTTPException(status_code=404, detail="No seller locations found")
        
        # In a real implementation, we would generate a map URL based on the seller locations
        # For now, returning the canonical URL as specified
        return "https://maps.example.com/sellers"
    finally:
        db.close()