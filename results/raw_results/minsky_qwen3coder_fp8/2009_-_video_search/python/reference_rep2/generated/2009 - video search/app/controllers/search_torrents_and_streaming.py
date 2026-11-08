from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal
from app.controllers.search_torrents import Torrent
from app.models._stubs import Streaming

router = APIRouter()

def search_torrents_and_streaming(query: str) -> dict[str, list[dict[str, str]]]:
    """
    The system processes the query string and returns search results relevant to the query from both torrent and streaming sources.

    Args:
        query: The search query string entered by the user in the shared search bar

    Returns:
        Search results from both torrent and streaming sources, formatted as a dictionary with keys 'torrents' and 'streaming'

    Notes:
        Postcondition: The search results displayed reflect the query entered by the user and include items from both torrent and streaming databases
        canonical call (must work): {"query":"pizza"}
        must return on success: {"torrents": [], "streaming": []}
        error mode: raise
    """
    db = SessionLocal()
    try:
        # Search for torrents matching the query
        torrent_results = db.query(Torrent).filter(Torrent.title.contains(query)).all()
        
        # Search for streaming items matching the query
        streaming_results = db.query(Streaming).filter(Streaming.title.contains(query)).all()
        
        # Format results
        torrents = [
            {
                "id": str(torrent.id),
                "title": torrent.title,
                "size": torrent.size,
                "seeders": str(torrent.seeders)
            }
            for torrent in torrent_results
        ]
        
        streaming = [
            {
                "id": str(streaming.id),
                "title": streaming.title,
                "duration": streaming.duration,
                "is_available": str(streaming.is_available)
            }
            for streaming in streaming_results
        ]
        
        return {
            "torrents": torrents,
            "streaming": streaming
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()