from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    quantity = Column(Integer)


router = APIRouter()


def format_order_items(items: list[dict[str, object]]) -> list[dict[str, object]]:
    """For each book in the order, the system displays the title of the book, its price, and the quantity purchased.

    Args:
        items: List of book items in an order, each item has title, price, and quantity

    Returns:
        List of formatted book details including title, price, and quantity

    Notes:
        Postcondition: Each displayed book in the order includes the title, price, and quantity, and nothing else
        Prerequisite: get_user_purchase_history (req 4.13.REQ-1) must have run first.
        canonical call (must work): {"items":[{"title":"Book Title","price":19.99,"quantity":2}]}
        must return on success: [{"title": "Book Title", "price": 19.99, "quantity": 2}]
        error_mode: raise

        precondition failure call (must raise HTTPException with a 4xx status): {"items":[]}
    """
    if not items:
        raise HTTPException(status_code=400, detail="No items provided")

    formatted_items = []
    for item in items:
        formatted_item = {
            "title": item["title"],
            "price": item["price"],
            "quantity": item["quantity"]
        }
        formatted_items.append(formatted_item)

    return formatted_items