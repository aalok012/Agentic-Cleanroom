from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class Book(Base):
    __tablename__ = "books"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    lending_option = Column(Boolean, nullable=False)
    selling_option = Column(Boolean, nullable=False)
    isbn = Column(String, nullable=False)
    author = Column(String, nullable=False)
    rental_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)

router = APIRouter()

@router.post("")
def validate_and_store_book_details(book_data: dict = Body(..., embed=True)) -> dict:
    # Validate the book data
    errors = []
    
    # Check required fields
    if not book_data.get("name") or not isinstance(book_data.get("name"), str):
        errors.append("Name is required and must be a string.")
    
    if not isinstance(book_data.get("quantity"), int) or book_data.get("quantity") <= 0:
        errors.append("Quantity must be a positive integer.")
    
    if not isinstance(book_data.get("lending_option"), bool):
        errors.append("Lending option must be a boolean.")
    
    if not isinstance(book_data.get("selling_option"), bool):
        errors.append("Selling option must be a boolean.")
    
    if not book_data.get("isbn") or not isinstance(book_data.get("isbn"), str):
        errors.append("ISBN is required and must be a string.")
    
    if not book_data.get("author") or not isinstance(book_data.get("author"), str):
        errors.append("Author is required and must be a string.")
    
    if not isinstance(book_data.get("rental_price"), (int, float)) or book_data.get("rental_price") < 0:
        errors.append("Rental price must be a non-negative number.")
    
    if not isinstance(book_data.get("selling_price"), (int, float)) or book_data.get("selling_price") < 0:
        errors.append("Selling price must be a non-negative number.")
    
    # Raise exception if validation fails
    if errors:
        raise HTTPException(status_code=400, detail="Validation failed: {}".format(", ".join(errors)))
    
    # If we reach here, validation passed
    db = SessionLocal()
    try:
        # Create new book instance
        new_book = Book(
            name=book_data["name"],
            quantity=book_data["quantity"],
            lending_option=book_data["lending_option"],
            selling_option=book_data["selling_option"],
            isbn=book_data["isbn"],
            author=book_data["author"],
            rental_price=book_data["rental_price"],
            selling_price=book_data["selling_price"]
        )
        
        # Add to database
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        
        return {"success": True, "errors": []}
    finally:
        db.close()