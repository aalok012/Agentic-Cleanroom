from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal


class SearchConfig(Base):
    __tablename__ = "search_config"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    include_torrents = Column(Boolean, default=False)


router = APIRouter()


@router.post("")
def toggle_torrent_search(include_torrents: bool = Body(..., embed=True)) -> None:
    db = SessionLocal()
    try:
        config = db.query(SearchConfig).first()
        if config is None:
            # Create new config if it doesn't exist
            config = SearchConfig(id=1, include_torrents=include_torrents)
            db.add(config)
        else:
            # Update existing config
            config.include_torrents = include_torrents
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to update search configuration")
    finally:
        db.close()