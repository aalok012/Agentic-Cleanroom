from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal


class PageButton(Base):
    __tablename__ = "page_buttons"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    label = Column(String(50))
    url = Column(String(255))


router = APIRouter()


@router.post("")
def fr_3_1_REQ_7(request: dict = Body(..., embed=True)) -> dict:
    db = SessionLocal()
    try:
        # Create a new page button entry in the database
        new_page_button = PageButton(label="Next", url="/next")
        db.add(new_page_button)
        db.commit()
        db.refresh(new_page_button)
        return {}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()