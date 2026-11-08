from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.models.store_user_information import User
    # Other user fields would be here

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.controllers.initiate_print_shop_search import PrintShop
    # Other print shop fields would be here

router = APIRouter()

@router.post("")
def initiate_print_request(user_id: str = Body(..., embed=True), print_shop_id: str = Body(..., embed=True)) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=403, detail="User is not registered or logged in")
        
        # Check if print shop exists
        print_shop = db.query(PrintShop).filter(PrintShop.id == print_shop_id).first()
        if not print_shop:
            raise HTTPException(status_code=404, detail="Print shop not found")
        
        # If we reach here, both user and print shop exist
        # The system transitions to a state where it awaits further input for the print job details
        return {"status": "initiated", "message": f"Print request process started for print shop {print_shop_id}"}
    finally:
        db.close()