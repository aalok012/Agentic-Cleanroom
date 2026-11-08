from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.models._stubs import Shipment

router = APIRouter()


def fr_4_12_REQ_3(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Assuming the request contains a shipment_id to identify the shipment
        shipment_id = request.get("shipment_id")
        if not shipment_id:
            raise HTTPException(status_code=400, detail="shipment_id is required")
        
        # Query the shipment from the database
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        
        # Return the required fields
        return {
            "shipping_date": shipment.shipping_date,
            "mailing_address": shipment.mailing_address,
            "projected_delivery_date": shipment.projected_delivery_date,
            "status": shipment.status
        }
    finally:
        db.close()