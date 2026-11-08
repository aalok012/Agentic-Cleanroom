from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal

class Registrant(Base):
    __tablename__ = "registrants"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

router = APIRouter()

def generate_registrant_list() -> list[dict[str, str]]:
    db = SessionLocal()
    try:
        registrants = db.query(Registrant).all()
        return [
            {"name": r.name, "email": r.email}
            for r in registrants
        ]
    finally:
        db.close()