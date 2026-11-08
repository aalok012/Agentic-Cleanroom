from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class SellerContact(Base):
    __tablename__ = "seller_contacts"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    seller_type = Column(String)
    contact_info = Column(String)

router = APIRouter()


def get_seller_contact_methods() -> list[dict[str, str]]:
    db = SessionLocal()
    try:
        contacts = db.query(SellerContact).all()
        result = []
        for contact in contacts:
            result.append({"type": contact.seller_type, "contact": contact.contact_info})
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to retrieve seller contact methods")
    finally:
        db.close()