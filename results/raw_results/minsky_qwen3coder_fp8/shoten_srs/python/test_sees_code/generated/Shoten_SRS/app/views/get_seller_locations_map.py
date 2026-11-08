from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.extensions import Base, SessionLocal


from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.test_sees_code.generated.Shoten_SRS.app.views.get_seller_details import Seller


router = APIRouter()


def get_seller_locations_map() -> str:
    db = SessionLocal()
    try:
        sellers = db.query(Seller).filter(
            (Seller.is_bookstore == True) | (Seller.is_printing_store == True)
        ).all()
        
        if not sellers:
            raise HTTPException(status_code=404, detail="No sellers found")
        
        # In a real implementation, we would generate a dynamic map URL
        # based on the seller locations
        return "https://maps.example.com/sellers"
    finally:
        db.close()