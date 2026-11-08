from fastapi import APIRouter, Body, HTTPException, status
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from datetime import datetime, timedelta
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.controllers.fr_4_12_REQ_2 import Order

class OrderStatus(Base):
    __tablename__ = "order_status"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    status = Column(String)
    updated_at = Column(DateTime, default=func.now())

router = APIRouter()


def fr_4_12_REQ_1(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Check if user is authenticated (simplified check)
        # In a real implementation, this would involve checking session or token
        user_id = request.get("user_id")
        if not user_id:
            raise HTTPException(status_code=403, detail="User not authenticated")
        
        # Calculate date 30 days ago
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        # Query orders placed within the last 30 days for the user
        orders = db.query(Order).filter(
            Order.user_id == user_id,
            Order.created_at >= thirty_days_ago
        ).all()
        
        # Return empty dict on success as per spec
        return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()