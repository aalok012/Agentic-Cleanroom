from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal


class Seller(Base):
    __tablename__ = "sellers"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    type = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)
    directions = Column(String)


router = APIRouter()


def get_seller_details() -> list[dict[str, str]]:
    db = SessionLocal()
    try:
        sellers = db.query(Seller).all()
        result = []
        for seller in sellers:
            result.append({
                "type": seller.type,
                "address": seller.address,
                "phone": seller.phone,
                "email": seller.email,
                "directions": seller.directions
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()