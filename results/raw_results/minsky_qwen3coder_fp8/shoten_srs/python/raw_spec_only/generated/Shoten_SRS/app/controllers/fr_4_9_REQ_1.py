from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_9_REQ_2 import Book

router = APIRouter()


def fr_4_9_REQ_1(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Validate request structure
        if "title" not in request or "author" not in request:
            raise HTTPException(status_code=400, detail="Title and author are required")
        
        # Create new book entry
        new_book = Book(
            title=request["title"],
            author=request["author"],
            price=request.get("price", 0.0),
            is_for_sale=request.get("is_for_sale", True),
            is_for_print=request.get("is_for_print", False),
            is_for_rent=request.get("is_for_rent", False)
        )
        
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        
        return {}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()