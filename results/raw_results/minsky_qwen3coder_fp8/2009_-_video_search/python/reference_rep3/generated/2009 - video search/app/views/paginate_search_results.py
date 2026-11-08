from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal


class SearchResult(Base):
    __tablename__ = "search_results"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    size = Column(String)


router = APIRouter()


def paginate_search_results(page_number: int, page_size: int, search_query: str) -> dict[str, list[dict[str, str]]]:
    if page_number <= 0:
        raise HTTPException(status_code=400, detail="Page number must be a positive integer.")
    
    if page_size <= 0:
        raise HTTPException(status_code=400, detail="Page size must be a positive integer.")
    
    if not search_query:
        raise HTTPException(status_code=400, detail="Search query must be a non-empty string.")
    
    db = SessionLocal()
    try:
        # Calculate offset for pagination
        offset = (page_number - 1) * page_size
        
        # Query the database for search results matching the query
        results = db.query(SearchResult).filter(SearchResult.name.contains(search_query)).offset(offset).limit(page_size).all()
        
        # Convert results to list of dictionaries
        result_list = []
        for item in results:
            result_list.append({"name": item.name, "size": item.size})
        
        # Count total results for pagination metadata
        total_results = db.query(SearchResult).filter(SearchResult.name.contains(search_query)).count()
        total_pages = (total_results + page_size - 1) // page_size
        
        return {
            "results": result_list,
            "page": page_number,
            "total_pages": total_pages
        }
    finally:
        db.close()