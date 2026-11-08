from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal
from app.controllers.search_torrents import Torrent
from app.models._stubs import Streaming

router = APIRouter()

def search_torrents_and_streaming(query: str) -> dict[str, list[dict[str, str]]]:
    """
    The system processes the query string and displays search results from both torrent and streaming sources in a unified result set.

    Args:
        query: The search query string entered by the user in the shared search bar

    Returns:
        A unified result set containing both torrent and streaming search results

    Notes:
        Postcondition: The displayed results accurately reflect the query string entered by the user, showing torrents and streaming content matching the search criteria
        canonical call (must work): {"query":"pizza"}
        must return on success: {"torrents": [], "streaming": []}
        error_mode: raise
    """
    db = SessionLocal()
    try:
        # Search for torrents matching the query
        torrents = db.query(Torrent).filter(Torrent.title.contains(query)).all()
        
        # Search for streaming content matching the query
        streaming = db.query(Streaming).filter(Streaming.title.contains(query)).all()
        
        # Convert to dictionaries
        torrents_result = [
            {
                "id": str(torrent.id),
                "title": torrent.title,
                "size": torrent.size,
                "seeders": str(torrent.seeders)
            }
            for torrent in torrents
        ]
        
        streaming_result = [
            {
                "id": str(streaming_item.id),
                "title": streaming_item.title,
                "type": streaming_item.type,
                "rating": str(streaming_item.rating)
            }
            for streaming_item in streaming
        ]
        
        return {
            "torrents": torrents_result,
            "streaming": streaming_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()