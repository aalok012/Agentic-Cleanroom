from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_9_REQ_2 import Book

title = "fr_4_3_1_REQ_1"
router = APIRouter()


class BookSearchRequest(Base):
    __tablename__ = "book_search_requests"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    isbn = Column(String)


def fr_4_3_1_REQ_1(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Extract search parameters from request
        search_title = request.get("title", None)
        search_author = request.get("author", None)
        search_isbn = request.get("isbn", None)

        # Build query based on provided search criteria
        query = db.query(Book)
        if search_title:
            query = query.filter(Book.title.contains(search_title))
        if search_author:
            query = query.filter(Book.author.contains(search_author))
        if search_isbn:
            query = query.filter(Book.isbn == search_isbn)

        # Execute query
        results = query.all()

        # Convert results to dictionary format
        books_list = []
        for book in results:
            books_list.append({
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "isbn": book.isbn,
                "price": float(book.price) if book.price else None,
                "in_stock": book.in_stock
            })

        return {"books": books_list}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()