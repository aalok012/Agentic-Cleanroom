from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal


class GoogleDriveLink(Base):
    __tablename__ = "google_drive_links"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)


router = APIRouter()


def fr_4_8_REQ_2(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Validate that the request contains the required fields
        if "url" not in request:
            raise HTTPException(status_code=400, detail="URL is required")
        
        # Create a new GoogleDriveLink entry
        db_link = GoogleDriveLink(url=request["url"])
        db.add(db_link)
        db.commit()
        db.refresh(db_link)
        
        return {}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()