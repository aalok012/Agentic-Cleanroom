from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.extensions import Base, SessionLocal


from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep3.generated.Shoten_SRS.app.controllers.validate_and_store_book_details import Book


router = APIRouter()


def display_purchased_books(purchase_details: dict[str, object]) -> list[dict[str, object]]:
    """
    System displays the titles, prices, and quantities of all books purchased.

    Args:
        purchase_details: Details of the successful purchase including purchased items with title, price, and quantity

    Returns:
        List of purchased books with their titles, prices, and quantities

    Raises:
        HTTPException: If the precondition is violated (Transaction is successfully processed and payment information is entered).

    Notes:
        Precondition: Transaction is successfully processed and payment information is entered
        Postcondition: The displayed information accurately reflects the books purchased, including their respective titles, prices, and quantities
        Prerequisite: process_purchase (req 4.7.REQ-1) must have run first.
    """
    # Check if purchase_details contains the required key
    if "purchased_items" not in purchase_details:
        raise HTTPException(status_code=400, detail="Invalid purchase details: missing purchased_items")

    # Validate that purchased_items is a list
    purchased_items = purchase_details["purchased_items"]
    if not isinstance(purchased_items, list):
        raise HTTPException(status_code=400, detail="Invalid purchase details: purchased_items must be a list")

    # Return the purchased items as they are already in the correct format
    return purchased_items