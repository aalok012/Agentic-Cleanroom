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

@router.post("")
def paginate_search_results(page_number: int = Body(..., embed=True), page_size: int = Body(..., embed=True), search_query: str = Body(..., embed=True)) -> dict[str, list[dict[str, str]]]:
    db = SessionLocal()
    try:
        # Validate inputs
        if page_number < 1:
            raise HTTPException(status_code=400, detail="Page number must be at least 1")
        if page_size <= 0:
            raise HTTPException(status_code=400, detail="Page size must be positive")
        
        # Calculate offset
        offset = (page_number - 1) * page_size
        
        # Query the database for paginated results
        results = db.query(SearchResult).filter(SearchResult.name.contains(search_query)).offset(offset).limit(page_size).all()
        
        # Format results as list of dictionaries
        formatted_results = []
        for result in results:
            formatted_results.append({"name": result.name, "size": result.size})
        
        return {"results": formatted_results}
    finally:
        db.close()