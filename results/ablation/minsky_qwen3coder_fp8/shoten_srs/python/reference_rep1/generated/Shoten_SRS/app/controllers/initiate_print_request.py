from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app.extensions import Base, SessionLocal

router = APIRouter()

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app.models.store_user_information import User
    # Other user fields would be here

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app.controllers.initiate_print_shop_search import PrintShop
    # Other print shop fields would be here

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep1.generated.Shoten_SRS.app.views.prompt_google_drive_url import PrintJob
    # Other print job fields would be here


def initiate_print_request(user_id: str, print_shop_id: str) -> dict[str, str]:
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
        
        # Create a new print job entry
        new_job = PrintJob(user_id=user_id, print_shop_id=print_shop_id)
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        
        return {
            "status": "initiated",
            "message": f"Print request process started for print shop {print_shop_id}"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()