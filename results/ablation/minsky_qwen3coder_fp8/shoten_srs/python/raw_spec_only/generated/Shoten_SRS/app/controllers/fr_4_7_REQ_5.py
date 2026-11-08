from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_9_REQ_2 import Book

type BookDict = dict[str, object]

router = APIRouter()


def fr_4_7_REQ_5(request: dict) -> dict:
    """On a successful transaction the books (titles and prices and quantities) will be displayed to the screen."""
    db = SessionLocal()
    try:
        books = db.query(Book).all()
        if not books:
            raise HTTPException(status_code=404, detail="No books found")
        
        books_data: list[BookDict] = []
        for book in books:
            books_data.append({
                "title": book.title,
                "price": book.price,
                "quantity": book.quantity
            })
        
        return {}
    finally:
        db.close()