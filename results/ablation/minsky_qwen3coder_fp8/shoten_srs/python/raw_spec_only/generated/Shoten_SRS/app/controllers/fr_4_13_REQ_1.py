from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from datetime import datetime, timedelta
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_1_REQ_2 import User
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.models._stubs import Purchase

class PurchaseModel(Base):
    __tablename__ = "purchases"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    amount = Column(Float)
    purchase_date = Column(DateTime)

router = APIRouter()


def fr_4_13_REQ_1(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Check if user is authenticated (simplified check)
        # In a real implementation, you would extract user info from the request context
        # For now, we assume the request contains user info
        user_id = request.get("user_id")
        if not user_id:
            raise HTTPException(status_code=403, detail="User not authenticated")
        
        # Calculate date two years ago
        two_years_ago = datetime.now() - timedelta(days=730)
        
        # Query purchases for the user within the last two years
        purchases = db.query(PurchaseModel).filter(
            PurchaseModel.user_id == user_id,
            PurchaseModel.purchase_date >= two_years_ago
        ).all()
        
        # Format the response
        result = []
        for purchase in purchases:
            result.append({
                "id": purchase.id,
                "amount": purchase.amount,
                "purchase_date": purchase.purchase_date.isoformat()
            })
        
        return {"purchases": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()