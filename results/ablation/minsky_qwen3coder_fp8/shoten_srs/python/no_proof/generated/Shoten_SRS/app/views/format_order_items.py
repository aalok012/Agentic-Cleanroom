from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal

router = APIRouter()

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.controllers.validate_and_store_book_details import Book

@router.post("")
def format_order_items(items: list[dict[str, object]] = Body(..., embed=True)) -> list[dict[str, object]]:
    if not items:
        raise HTTPException(status_code=400, detail="No items provided")
    
    # Validate each item has required fields
    for item in items:
        if not all(key in item for key in ["title", "price", "quantity"]):
            raise HTTPException(status_code=400, detail="Each item must include title, price, and quantity")
    
    # Return the formatted items as specified
    return [
        {
            "title": item["title"],
            "price": item["price"],
            "quantity": item["quantity"]
        }
        for item in items
    ]
