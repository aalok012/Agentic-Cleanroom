from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal


class Torrent(Base):
    __tablename__ = "torrents"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    seeds = Column(Integer)
    peers = Column(Integer)
    size = Column(String)
    date_posted = Column(String)
    webpage_link = Column(String)


router = APIRouter()


def search_torrents(query: str) -> list[dict[str, str]]:
    db = SessionLocal()
    try:
        results = (
            db.query(Torrent)
            .filter(Torrent.name.contains(query))
            .all()
        )
        if not results:
            raise HTTPException(status_code=404, detail="No torrents found")
        
        torrent_list = []
        for torrent in results:
            torrent_list.append({
                "seeds": str(torrent.seeds),
                "peers": str(torrent.peers),
                "size": torrent.size,
                "date_posted": torrent.date_posted,
                "webpage_link": torrent.webpage_link
            })
        
        return torrent_list
    finally:
        db.close()