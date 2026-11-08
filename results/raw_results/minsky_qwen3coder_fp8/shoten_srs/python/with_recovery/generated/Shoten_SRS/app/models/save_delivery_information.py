from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class DeliveryInformation(Base):
    __tablename__ = "delivery_information"
    __table_args__ = {"extend_existing": True}
    
    user_id = Column(String, primary_key=True)
    street = Column(String)
    city = Column(String)
    zip_code = Column(String)

router = APIRouter()

def _check_user_purchase_state(user_id: str) -> None:
    # Placeholder for actual purchase state validation
    # In a real implementation, this would check if the user is in the delivery info step
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

@router.post("")
def save_delivery_information(user_id: str = Body(..., embed=True), delivery_info: dict[str, str] = Body(..., embed=True)) -> bool:
    db = SessionLocal()
    try:
        # Check if user has initiated the purchase process
        _check_user_purchase_state(user_id)
        
        # Create or update delivery information
        existing_record = db.query(DeliveryInformation).filter(DeliveryInformation.user_id == user_id).first()
        
        if existing_record:
            # Update existing record
            for key, value in delivery_info.items():
                if hasattr(existing_record, key):
                    setattr(existing_record, key, value)
        else:
            # Create new record
            new_record = DeliveryInformation(
                user_id=user_id,
                **delivery_info
            )
            db.add(new_record)
        
        db.commit()
        return True
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save delivery information")
    finally:
        db.close()