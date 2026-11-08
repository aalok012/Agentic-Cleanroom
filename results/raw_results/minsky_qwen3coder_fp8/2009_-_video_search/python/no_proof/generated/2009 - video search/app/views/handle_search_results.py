from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal

router = APIRouter()

def handle_search_results(results: list) -> str:
    """
    Display the message "No results were found for this search.".

    Args:
        results: The list of search results returned by the search operation. If empty, the no-results message should be displayed.

    Returns:
        The message 'No results were found for this search.' if results is empty, otherwise an empty string.

    Notes:
        Postcondition: The message "No results were found for this search." is shown to the user as a result of the search operation
        canonical call (must work): {"results":[]}
        must return on success: "No results were found for this search."
        error_mode: raise
    """
    if not results:
        return "No results were found for this search."
    else:
        return ""
