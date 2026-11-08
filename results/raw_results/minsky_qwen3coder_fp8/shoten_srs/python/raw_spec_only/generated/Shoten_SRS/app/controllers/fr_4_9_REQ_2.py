from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class Book(Base):
    __tablename__ = "books"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    lendable = Column(Boolean, nullable=False)
    sellable = Column(Boolean, nullable=False)
    isbn = Column(String, nullable=False)
    author = Column(String, nullable=False)
    rental_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)

router = APIRouter()

@router.post("")
def fr_4_9_REQ_2(request: dict = Body(..., embed=True)) -> dict:
    db = SessionLocal()
    try:
        # Extract book details from request
        book_data = {
            "name": request.get("name"),
            "quantity": request.get("quantity"),
            "lendable": request.get("options", {}).get("lending"),
            "sellable": request.get("options", {}).get("selling"),
            "isbn": request.get("isbn"),
            "author": request.get("author"),
            "rental_price": request.get("price_on_rental_basis"),
            "selling_price": request.get("price_for_selling")
        }
        
        # Validate required fields
        if not all([book_data["name"], book_data["quantity"], book_data["isbn"], book_data["author"], book_data["rental_price"], book_data["selling_price"]]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Create new book instance
        new_book = Book(**book_data)
        
        # Add to database
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        
        return {}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()