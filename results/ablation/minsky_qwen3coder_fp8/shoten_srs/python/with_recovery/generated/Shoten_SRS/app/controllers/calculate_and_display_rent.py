from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class CartItem(Base):
    __tablename__ = "cart_items"
    __table_args__ = {"extend_existing": True}
    user_id = Column(Integer)
    book_id = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

router = APIRouter()


def initiate_rental_process(user_id: str, cart_items: list[dict[str, str]]) -> bool:
    db = SessionLocal()
    try:
        for item in cart_items:
            db_item = CartItem(
                title=item["title"],
                price=item["price"],
                quantity=1,
                user_id=user_id
            )
            db.add(db_item)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@router.post("")
def calculate_and_display_rent(
    cart_items: list[dict[str, str]] = Body(..., embed=True),
    rental_duration: str = Body(..., embed=True)
) -> dict[str, float]:
    # Validate rental duration
    valid_durations = ["1 week", "2 weeks", "1 month"]
    if rental_duration not in valid_durations:
        raise HTTPException(status_code=400, detail="Invalid rental period")

    # Validate cart items
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Calculate individual rents
    individual_rents = []
    total_rent = 0.0

    for item in cart_items:
        # Assuming a simple calculation where rent is price * quantity
        # In a real scenario, this would involve more complex logic based on rental duration
        rent = item["price"] * item["quantity"]
        individual_rents.append({"title": item["title"], "rent": rent})
        total_rent += rent

    return {
        "total_rent": round(total_rent, 2),
        "individual_rents": individual_rents
    }