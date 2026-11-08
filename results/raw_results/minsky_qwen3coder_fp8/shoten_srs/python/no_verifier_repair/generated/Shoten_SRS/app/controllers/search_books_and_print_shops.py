from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal


from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.controllers.validate_and_store_book_details import Book


from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.controllers.initiate_print_shop_search import PrintShop


router = APIRouter()


def search_books_and_print_shops(query: str) -> list[dict[str, str]]:
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    db = SessionLocal()
    try:
        # Search for books
        books = (
            db.query(Book)
            .filter(Book.title.contains(query) | Book.author.contains(query))
            .all()
        )

        # Search for print shops
        print_shops = (
            db.query(PrintShop)
            .filter(PrintShop.name.contains(query) | PrintShop.location.contains(query))
            .all()
        )

        # Format results
        results = []
        for book in books:
            results.append({"title": book.title, "type": "book"})
        
        for shop in print_shops:
            results.append({"name": shop.name, "type": "print_shop"})

        return results
    finally:
        db.close()