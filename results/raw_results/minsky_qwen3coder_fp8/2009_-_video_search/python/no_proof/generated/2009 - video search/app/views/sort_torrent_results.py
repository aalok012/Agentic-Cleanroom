from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal

router = APIRouter()

class TorrentResult(Base):
    __tablename__ = "torrent_results"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    size = Column(String)
    date = Column(String)

@router.post("")
def sort_torrent_results(results: list[dict[str, str]] = Body(..., embed=True), sort_by: str = Body(..., embed=True)) -> list[dict[str, str]]:
    # Validate sort_by parameter
    valid_sort_options = ["size", "date", "alphabetical"]
    if sort_by not in valid_sort_options:
        raise HTTPException(status_code=400, detail="Invalid sort_by parameter")

    # Handle empty results case
    if not results:
        return []

    # Sort based on the sort_by parameter
    if sort_by == "size":
        # For size sorting, we need to extract numeric values
        def size_to_numeric(size_str):
            size_str = size_str.upper()
            if "GB" in size_str:
                return float(size_str.replace("GB", "")) * 1024
            elif "MB" in size_str:
                return float(size_str.replace("MB", ""))
            elif "KB" in size_str:
                return float(size_str.replace("KB", "")) / 1024
            else:
                return float(size_str)
        
        return sorted(results, key=lambda x: size_to_numeric(x["size"]), reverse=True)
    
    elif sort_by == "date":
        # Sort by date (newest first)
        return sorted(results, key=lambda x: x["date"], reverse=True)
    
    elif sort_by == "alphabetical":
        # Sort alphabetically by name
        return sorted(results, key=lambda x: x["name"])
    
    # This should never happen due to validation above
    raise HTTPException(status_code=400, detail="Invalid sort_by parameter")