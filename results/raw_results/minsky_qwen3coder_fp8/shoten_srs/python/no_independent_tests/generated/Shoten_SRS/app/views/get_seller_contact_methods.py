from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class SellerContact(Base):
    __tablename__ = "seller_contacts"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    seller_type = Column(String, nullable=False)
    contact_method = Column(String, nullable=False)

router = APIRouter()


def get_seller_contact_methods() -> dict[str, list[str]]:
    db = SessionLocal()
    try:
        contacts = db.query(SellerContact).all()
        result = {"bookstore": [], "printstore": [], "student": []}
        for contact in contacts:
            if contact.seller_type in result:
                result[contact.seller_type].append(contact.contact_method)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve seller contact methods")
    finally:
        db.close()