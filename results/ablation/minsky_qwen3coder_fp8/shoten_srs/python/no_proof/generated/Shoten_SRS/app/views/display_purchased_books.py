from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.controllers.validate_and_store_book_details import Book

router = APIRouter()

@router.post("")
def display_purchased_books(purchased_items: list[dict[str, object]] = Body(..., embed=True)) -> list[dict[str, object]]:
    if not purchased_items:
        raise HTTPException(status_code=400, detail="No purchased items provided")

    # Validate each item has required fields
    for item in purchased_items:
        if not all(key in item for key in ["title", "price", "quantity"]):
            raise HTTPException(status_code=400, detail="Each item must have title, price, and quantity")

    # Simulate database interaction - in real app, this would query the DB
    db = SessionLocal()
    try:
        # Here we would normally fetch the actual book data from the database
        # For now, we'll just return the input as per the spec
        return purchased_items
    finally:
        db.close()