from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal

class Torrent(Base):
    __tablename__ = "torrents"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    seeds = Column(Integer)
    peers = Column(Integer)
    size = Column(String)
    date_posted = Column(String)
    link = Column(String)

router = APIRouter()

@router.post("")
def search_torrents(query: str = Body(..., embed=True)) -> list[dict[str, str]]:
    db = SessionLocal()
    try:
        results = db.query(Torrent).filter(Torrent.id.like(f"%{query}%")).all()
        if not results:
            raise HTTPException(status_code=404, detail="No torrents found for the given query")
        
        response = []
        for result in results:
            response.append({
                "seeds": str(result.seeds),
                "peers": str(result.peers),
                "size": result.size,
                "date_posted": result.date_posted,
                "link": result.link
            })
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()