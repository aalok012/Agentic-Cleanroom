from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_1_REQ_2 import User

router = APIRouter()

@router.post("")
def fr_4_1_REQ_3(request: dict = Body(..., embed=True)) -> dict:
    db = SessionLocal()
    try:
        # Generate a unique username
        username = f"user_{db.query(User).count() + 1}"
        
        # Create a new user with the generated username
        new_user = User(username=username, password=None)  # Password will be set later
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Return empty dict as per spec
        return {}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()