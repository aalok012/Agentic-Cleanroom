from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal


class DeliveryInfo(Base):
    __tablename__ = "delivery_info"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country = Column(String, nullable=False)


router = APIRouter()


def fr_4_7_REQ_3(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Validate request structure
        if not isinstance(request, dict):
            raise HTTPException(status_code=400, detail="Invalid request structure")
        
        # Extract delivery info from request
        delivery_data = request.get("delivery_info", {})
        
        # Validate required fields
        required_fields = ["name", "address", "city", "postal_code", "country"]
        for field in required_fields:
            if field not in delivery_data or not delivery_data[field]:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Create new delivery info entry
        new_delivery_info = DeliveryInfo(
            name=delivery_data["name"],
            address=delivery_data["address"],
            city=delivery_data["city"],
            postal_code=delivery_data["postal_code"],
            country=delivery_data["country"]
        )
        
        # Save to database
        db.add(new_delivery_info)
        db.commit()
        db.refresh(new_delivery_info)
        
        return {}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()