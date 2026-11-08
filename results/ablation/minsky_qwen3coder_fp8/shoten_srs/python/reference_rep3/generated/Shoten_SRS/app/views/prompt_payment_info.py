from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class PurchaseProcess(Base):
    __tablename__ = "purchase_processes"
    __table_args__ = {"extend_existing": True}
    
    user_id = Column(String, primary_key=True)
    completed = Column(Boolean, default=False)
    delivery_entered = Column(Boolean, default=False)
    

def prompt_payment_info(user_id: str) -> dict[str, str]:
    db = SessionLocal()
    try:
        # Check if the purchase process is completed and delivery info is entered
        purchase = db.query(PurchaseProcess).filter(PurchaseProcess.user_id == user_id).first()
        
        if not purchase or not purchase.completed or not purchase.delivery_entered:
            raise HTTPException(status_code=400, detail="Precondition violated: Purchase process is not completed or delivery information not entered.")
        
        return {"message": "Please enter your payment information"}
    finally:
        db.close()

router = APIRouter()

@router.post("")
def _prompt_payment_info(
    user_id: str = Body(..., embed=True)
):
    return prompt_payment_info(user_id)