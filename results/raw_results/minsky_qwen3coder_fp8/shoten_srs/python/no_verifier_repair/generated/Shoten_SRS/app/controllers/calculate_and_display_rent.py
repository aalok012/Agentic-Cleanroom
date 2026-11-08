from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal


class CartItem(Base):
    __tablename__ = "cart_items"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    rental_duration = Column(String)


router = APIRouter()


def calculate_and_display_rent(
    cart_items: list[dict[str, str]],
    rental_duration: str,
) -> dict[str, float]:
    # Validate rental duration
    valid_durations = ["1 week", "2 weeks", "1 month"]
    if rental_duration not in valid_durations:
        raise HTTPException(status_code=400, detail="Invalid rental period")

    # Validate cart items
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    db = SessionLocal()
    try:
        # Create CartItem objects and save them to the database
        db_cart_items = []
        for item in cart_items:
            db_item = CartItem(
                title=item["title"],
                price=item["price"],
                quantity=item["quantity"],
                rental_duration=rental_duration,
            )
            db.add(db_item)
            db_cart_items.append(db_item)
        db.commit()

        # Calculate rents
        total_rent = 0.0
        individual_rents = []
        for item in db_cart_items:
            rent = item.price * item.quantity
            total_rent += rent
            individual_rents.append({"title": item.title, "rent": rent})

        return {"total_rent": total_rent, "individual_rents": individual_rents}
    finally:
        db.close()