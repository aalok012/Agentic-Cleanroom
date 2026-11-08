from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal


class OperationInfo(Base):
    __tablename__ = "operation_info"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    operation_name = Column(String, nullable=False)
    usage_info = Column(String, nullable=False)


router = APIRouter()


def fr_4_15_REQ_3(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Since the requirement is self-contained and doesn't specify which operation,
        # we'll return generic usage info.
        # In a real implementation, this would fetch specific operation info from DB.
        operation_info = db.query(OperationInfo).filter_by(operation_name="generic").first()
        if not operation_info:
            # If no generic info exists, create it
            operation_info = OperationInfo(
                operation_name="generic",
                usage_info="To use this operation, provide the required parameters as specified in the API documentation."
            )
            db.add(operation_info)
            db.commit()
            db.refresh(operation_info)
        
        return {"usage_info": operation_info.usage_info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()