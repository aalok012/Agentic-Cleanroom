from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal

class FileModel(Base):
    __tablename__ = "files"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    seed_count = Column(Integer)
    peer_count = Column(Integer)
    file_size = Column(Float)
    date_posted = Column(String)
    webpage_link = Column(String)
    name = Column(String)
    size = Column(Integer)
    date = Column(String)

router = APIRouter()


def fr_3_1_REQ_4(request: dict) -> dict:
    db = SessionLocal()
    try:
        # Assuming we're querying for a specific file ID, which should be passed in the request
        file_id = request.get("file_id")
        if file_id is None:
            raise HTTPException(status_code=400, detail="Missing file_id in request")
        
        file_record = db.query(FileModel).filter(FileModel.id == file_id).first()
        if file_record is None:
            raise HTTPException(status_code=404, detail="File not found")
        
        result = {
            "seed_count": file_record.seed_count,
            "peer_count": file_record.peer_count,
            "file_size": file_record.file_size,
            "date_posted": file_record.date_posted,
            "webpage_link": file_record.webpage_link
        }
        
        return result
    finally:
        db.close()