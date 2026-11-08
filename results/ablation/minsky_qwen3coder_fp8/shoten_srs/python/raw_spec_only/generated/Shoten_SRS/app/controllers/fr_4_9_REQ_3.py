from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal


class PaymentDetails(Base):
    __tablename__ = "payment_details"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    bank_account_number = Column(String, nullable=False)
    ifsc_code = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


router = APIRouter()


def fr_4_9_REQ_3(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Validate request structure
        if "user_id" not in request:
            raise HTTPException(status_code=400, detail="user_id is required")
        if "bank_account_number" not in request:
            raise HTTPException(status_code=400, detail="bank_account_number is required")
        if "ifsc_code" not in request:
            raise HTTPException(status_code=400, detail="ifsc_code is required")

        # Create new payment details entry
        payment_detail = PaymentDetails(
            user_id=request["user_id"],
            bank_account_number=request["bank_account_number"],
            ifsc_code=request["ifsc_code"],
            is_active=True,
        )

        db.add(payment_detail)
        db.commit()
        db.refresh(payment_detail)

        return {}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()