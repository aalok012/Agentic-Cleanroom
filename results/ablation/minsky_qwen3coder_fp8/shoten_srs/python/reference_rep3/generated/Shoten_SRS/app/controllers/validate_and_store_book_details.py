from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal

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
    # Validate preconditions
    if not book_data or not isinstance(book_data, dict):
        raise HTTPException(status_code=400, detail="Invalid book data provided")

    # Check required fields
    required_fields = [
        "name", "quantity", "lending_option", "selling_option", 
        "isbn", "author", "rental_price", "selling_price"
    ]
    for field in required_fields:
        if field not in book_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

    # Validate specific field types
    if not isinstance(book_data["name"], str) or not book_data["name"].strip():
        raise HTTPException(status_code=400, detail="Name must be a non-empty string")
    if not isinstance(book_data["quantity"], int) or book_data["quantity"] <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be a positive integer")
    if not isinstance(book_data["lending_option"], bool):
        raise HTTPException(status_code=400, detail="Lending option must be a boolean")
    if not isinstance(book_data["selling_option"], bool):
        raise HTTPException(status_code=400, detail="Selling option must be a boolean")
    if not isinstance(book_data["isbn"], str) or not book_data["isbn"].strip():
        raise HTTPException(status_code=400, detail="ISBN must be a non-empty string")
    if not isinstance(book_data["author"], str) or not book_data["author"].strip():
        raise HTTPException(status_code=400, detail="Author must be a non-empty string")
    if not isinstance(book_data["rental_price"], (int, float)) or book_data["rental_price"] < 0:
        raise HTTPException(status_code=400, detail="Rental price must be a non-negative number")
    if not isinstance(book_data["selling_price"], (int, float)) or book_data["selling_price"] < 0:
        raise HTTPException(status_code=400, detail="Selling price must be a non-negative number")

    # Open database session
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
        
        # Add to session and commit
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        
        # Return success response
        return {"status": "success", "book_id": f"book{new_book.id}"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to store book details")
    finally:
        db.close()