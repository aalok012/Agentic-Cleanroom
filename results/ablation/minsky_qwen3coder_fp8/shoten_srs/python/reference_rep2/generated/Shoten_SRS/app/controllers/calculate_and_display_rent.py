from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.views.prompt_rental_period import ShoppingCart
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.controllers.validate_and_store_book_details import Book

class Rental(Base):
    __tablename__ = "rentals"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    book_title = Column(String)
    rent_amount = Column(Float)

router = APIRouter()


def calculate_and_display_rent(user_id: str, rental_period: str) -> dict[str, float]:
    db = SessionLocal()
    try:
        # Validate rental period
        valid_periods = ["1 week", "2 weeks", "1 month"]
        if rental_period not in valid_periods:
            raise HTTPException(status_code=400, detail="Invalid rental period")
        
        # Get shopping cart items for the user
        cart_items = db.query(ShoppingCart).filter_by(user_id=user_id).all()
        
        if not cart_items:
            raise HTTPException(status_code=404, detail="No items in shopping cart")
        
        # Calculate individual rents and total rent
        individual_rents = []
        total_rent = 0.0
        
        for item in cart_items:
            # Get book details
            book = db.query(Book).filter_by(title=item.book_title).first()
            if not book:
                raise HTTPException(status_code=404, detail=f"Book {item.book_title} not found")
            
            # Calculate rent based on rental period
            # Assuming rent is proportional to price and period
            rent = book.price
            if rental_period == "2 weeks":
                rent *= 2
            elif rental_period == "1 month":
                rent *= 4
            
            individual_rents.append({"title": item.book_title, "rent": round(rent, 2)})
            total_rent += rent
        
        return {
            "total_rent": round(total_rent, 2),
            "individual_rents": individual_rents
        }
    finally:
        db.close()