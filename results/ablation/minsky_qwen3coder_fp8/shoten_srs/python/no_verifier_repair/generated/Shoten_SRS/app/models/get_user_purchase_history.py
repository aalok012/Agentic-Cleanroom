from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal
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

@router.post("")
def get_user_purchase_history(user_id: str = Body(..., embed=True), days_back: int = Body(..., embed=True)) -> list[dict[str, object]]:
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID cannot be empty")
    
    db = SessionLocal()
    try:
        # Calculate the date threshold
        threshold_date = datetime.utcnow() - timedelta(days=days_back)
        
        # Query purchases for the user within the specified time frame
        purchases = db.query(Purchase).filter(
            Purchase.user_id == user_id,
            Purchase.date >= threshold_date
        ).all()
        
        # Convert to list of dictionaries
        result = []
        for purchase in purchases:
            result.append({
                "id": purchase.id,
                "date": purchase.date.strftime("%Y-%m-%d"),
                "payment_mode": purchase.payment_mode,
                "items": eval(purchase.items)  # Assuming items are stored as string representation of list
            })
        
        return result
    finally:
        db.close()