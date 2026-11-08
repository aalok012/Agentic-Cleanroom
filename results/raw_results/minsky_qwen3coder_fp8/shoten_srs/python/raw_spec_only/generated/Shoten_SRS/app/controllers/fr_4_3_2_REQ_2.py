from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal


from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_3_2_REQ_1 import PrintShop


router = APIRouter()


def fr_4_3_2_REQ_2(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Query all print shops from the database
        print_shops = db.query(PrintShop).all()
        
        # Prepare the response with required fields
        result = []
        for shop in print_shops:
            result.append({
                "name": shop.name,
                "opening_time": shop.opening_time,
                "closing_time": shop.closing_time,
                "rate": shop.rate
            })
        
        return {"print_shops": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()