from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class PrintShop(Base):
    __tablename__ = "print_shops"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    rating = Column(Float)
    is_active = Column(Boolean)

router = APIRouter()


def fr_4_3_2_REQ_1(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Since the request is empty, we'll return all active print shops
        print_shops = db.query(PrintShop).filter(PrintShop.is_active == True).all()
        
        # Convert to list of dictionaries
        result = []
        for shop in print_shops:
            result.append({
                "id": shop.id,
                "name": shop.name,
                "address": shop.address,
                "rating": shop.rating
            })
        
        return {"print_shops": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()