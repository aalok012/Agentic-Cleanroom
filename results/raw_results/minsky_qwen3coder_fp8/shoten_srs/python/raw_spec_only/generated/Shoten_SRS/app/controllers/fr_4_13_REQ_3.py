from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_12_REQ_2 import Order
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_9_REQ_2 import Book

table_name = "order_books"

class OrderBook(Base):
    __tablename__ = table_name
    __table_args__ = {"extend_existing": True}
    
    order_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

router = APIRouter()


def fr_4_13_REQ_3(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Extract order_id from request
        order_id = request.get("order_id")
        if not order_id:
            raise HTTPException(status_code=400, detail="Missing order_id in request")
        
        # Fetch the order
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Fetch order books with book details
        order_books = db.query(OrderBook, Book).join(Book, OrderBook.book_id == Book.id).filter(OrderBook.order_id == order_id).all()
        
        # Prepare response
        result = []
        for order_book, book in order_books:
            result.append({
                "title": book.title,
                "price": order_book.price,
                "quantity": order_book.quantity
            })
        
        return {"books": result}
    finally:
        db.close()