from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_1_REQ_2 import User

router = APIRouter()


def fr_4_1_REQ_1(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == request.get("username")).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Create new user
        new_user = User(
            username=request.get("username"),
            email=request.get("email"),
            hashed_password=request.get("hashed_password")
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()