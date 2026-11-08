from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.controllers.validate_and_store_book_details import Book

router = APIRouter()


def search_books(query: str) -> list[dict[str, str | int | bool]]:
    """Display list of matching books with picture of the front cover, along with the title, author, price, availability, and condition of the book.

    Args:
        query: The search query string for title, author, or ISBN

    Returns:
        List of matching books with details
    """
    db = SessionLocal()
    try:
        # Search for books matching the query in title, author, or ISBN
        books = db.query(Book).filter(
            (Book.title.contains(query)) |
            (Book.author.contains(query)) |
            (Book.isbn.contains(query))
        ).all()

        # Convert to list of dictionaries with required fields
        result = []
        for book in books:
            result.append({
                "title": book.title,
                "author": book.author,
                "isbn": book.isbn,
                "cover_image": book.cover_image,
                "price": book.price,
                "availability": book.availability,
                "condition": book.condition
            })

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error searching books: {str(e)}")
    finally:
        db.close()