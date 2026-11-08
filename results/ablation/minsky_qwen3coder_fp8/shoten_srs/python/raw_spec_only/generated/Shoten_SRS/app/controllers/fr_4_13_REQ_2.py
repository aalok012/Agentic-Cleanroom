from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.models._stubs import Purchase

router = APIRouter()


def fr_4_13_REQ_2(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Query all purchases to display date of purchase and payment mode
        purchases = db.query(Purchase).all()
        
        # Prepare the response with required fields
        result = []
        for purchase in purchases:
            result.append({
                "date_of_purchase": purchase.date_of_purchase,
                "payment_mode": purchase.payment_mode
            })
        
        return {}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()