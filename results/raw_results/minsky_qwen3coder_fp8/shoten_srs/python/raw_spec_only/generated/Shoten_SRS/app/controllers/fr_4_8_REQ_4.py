from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_7_REQ_3 import DeliveryInfo

router = APIRouter()


def fr_4_8_REQ_4(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Create a new delivery info entry
        delivery_info = DeliveryInfo(**request)
        db.add(delivery_info)
        db.commit()
        db.refresh(delivery_info)
        return {}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()