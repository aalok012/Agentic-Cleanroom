from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal


class Operation(Base):
    __tablename__ = "operations"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


router = APIRouter()


def get_help_overview() -> dict[str, list[dict[str, str]]]:
    db = SessionLocal()
    try:
        operations = db.query(Operation).all()
        result = [
            {"name": op.name, "description": op.description}
            for op in operations
        ]
        return {"operations": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()