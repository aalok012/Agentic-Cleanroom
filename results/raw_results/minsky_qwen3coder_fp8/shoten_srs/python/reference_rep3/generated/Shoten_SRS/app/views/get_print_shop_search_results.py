from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal


from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.controllers.initiate_print_shop_search import PrintShop


router = APIRouter()


def get_print_shop_search_results() -> list[dict[str, str | int | float]]:
    db = SessionLocal()
    try:
        # Check if search has been initiated and results are ready
        # For this implementation, we assume the search is always ready
        # In a real application, this would involve checking a search status table
        
        # Query the print shops from the database
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
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error retrieving print shop search results")
    finally:
        db.close()