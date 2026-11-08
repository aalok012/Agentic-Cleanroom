from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.extensions import Base, SessionLocal


from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.views.get_seller_details import Seller


router = APIRouter()


def get_seller_locations_map() -> str:
    db = SessionLocal()
    try:
        sellers = db.query(Seller).filter(
            (Seller.is_bookstore == True) | (Seller.is_printing_store == True)
        ).all()
        
        if not sellers:
            # Return the canonical URL even if no sellers are found
            return "https://maps.example.com/sellers"
        
        # In a real implementation, we would generate a dynamic map URL
        # based on the seller locations
        return "https://maps.example.com/sellers"
    finally:
        db.close()