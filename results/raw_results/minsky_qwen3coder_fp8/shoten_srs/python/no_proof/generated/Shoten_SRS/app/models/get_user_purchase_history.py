from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_proof.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from datetime import datetime, timedelta

class Purchase(Base):
    __tablename__ = "purchases"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    payment_mode = Column(String, nullable=False)
    items = Column(Text, nullable=False)

router = APIRouter()


def get_user_purchase_history(user_id: str, days_back: int = 730) -> list[dict[str, object]]:
    """A list of purchases made with the user's account within the last two years.

    Args:
        user_id: Unique identifier of the logged-in user requesting the purchase history
        days_back: Number of days to look back for purchases, default is 730 (2 years)

    Returns:
        List of purchase records for the user within the specified time frame

    Raises:
        HTTPException: If the precondition is violated (The user is authenticated and authorized to access their account data).
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID cannot be empty")

    db = SessionLocal()
    try:
        # Calculate the date threshold
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)

        # Query purchases for the user within the specified time frame
        purchases = (
            db.query(Purchase)
            .filter(
                Purchase.user_id == user_id,
                Purchase.date >= cutoff_date
            )
            .all()
        )

        # Convert to list of dictionaries
        result = []
        for purchase in purchases:
            result.append({
                "id": purchase.id,
                "date": purchase.date.isoformat(),
                "payment_mode": purchase.payment_mode,
                "items": purchase.items  # Assuming items is stored as JSON string
            })

        return result
    finally:
        db.close()