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
def paginate_search_results(
    page_number: int = Body(..., embed=True),
    page_size: int = Body(..., embed=True),
    search_query: str = Body(..., embed=True),
) -> dict[str, list[dict[str, str]]]:
    db = SessionLocal()
    try:
        offset = (page_number - 1) * page_size
        results = (
            db.query(SearchResult)
            .filter(SearchResult.name.contains(search_query))
            .offset(offset)
            .limit(page_size)
            .all()
        )
        
        # Convert the SQLAlchemy objects to dictionaries
        result_dicts = [
            {"name": result.name, "size": result.size}
            for result in results
        ]
        
        return {"results": result_dicts}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()