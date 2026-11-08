from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.controllers.initiate_print_shop_search import PrintShop

router = APIRouter()


def get_print_shop_search_results() -> list[dict[str, str | int | float]]:
    db = SessionLocal()
    try:
        # Check if search has been initiated and results are ready
        # This is a placeholder check - in reality, this would involve checking
        # some kind of search status in the database
        search_initiated = True  # Placeholder logic
        
        if not search_initiated:
            raise HTTPException(status_code=400, detail="Search has not been initiated or results are not ready")
        
        # Query print shops from the database
        print_shops = db.query(PrintShop).all()
        
        # Convert to list of dictionaries
        result = []
        for shop in print_shops:
            result.append({
                "name": shop.name,
                "opening_time": shop.opening_time,
                "closing_time": shop.closing_time,
                "rate_per_page": shop.rate_per_page
            })
        
        return result
    finally:
        db.close()