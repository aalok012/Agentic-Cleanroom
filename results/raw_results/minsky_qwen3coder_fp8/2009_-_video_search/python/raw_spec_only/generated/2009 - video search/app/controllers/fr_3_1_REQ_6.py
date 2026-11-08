from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal


from app.controllers.fr_3_1_REQ_4 import FileModel as File


router = APIRouter()


def fr_3_1_REQ_6(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Extract sorting parameters from request
        sort_by = request.get("sort_by", "name")
        sort_order = request.get("sort_order", "asc")
        
        # Validate sort_by
        valid_columns = ["name", "size", "date"]
        if sort_by not in valid_columns:
            raise HTTPException(status_code=400, detail="Invalid sort column")
        
        # Validate sort_order
        if sort_order not in ["asc", "desc"]:
            raise HTTPException(status_code=400, detail="Invalid sort order")
        
        # Build query based on sort parameters
        query = db.query(File)
        
        # Apply sorting
        if sort_by == "name":
            if sort_order == "asc":
                query = query.order_by(File.name.asc())
            else:
                query = query.order_by(File.name.desc())
        elif sort_by == "size":
            if sort_order == "asc":
                query = query.order_by(File.size.asc())
            else:
                query = query.order_by(File.size.desc())
        elif sort_by == "date":
            if sort_order == "asc":
                query = query.order_by(File.date.asc())
            else:
                query = query.order_by(File.date.desc())
        
        # Execute query
        results = query.all()
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "name": result.name,
                "size": result.size,
                "date": result.date
            })
        
        return {"results": formatted_results}
    finally:
        db.close()