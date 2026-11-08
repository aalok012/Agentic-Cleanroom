from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.controllers.validate_and_store_book_details import Book

router = APIRouter()

def calculate_shopping_cart_total(cart_items: list[dict[str, object]]) -> float:
    """
    System displays the total cost of all books in the shopping cart.

    Args:
        cart_items: List of book items in the shopping cart, each with 'price' and 'quantity' fields

    Returns:
        Total cost of all books in the shopping cart

    Raises:
        HTTPException: If the precondition is violated (Shopping cart contains at least one book).

    Notes:
        Precondition: Shopping cart contains at least one book
        Postcondition: The displayed total cost accurately reflects the sum of (price * quantity) for all books in the shopping cart
        canonical call (must work): {"cart_items":[{"price":10.99,"quantity":2},{"price":5.5,"quantity":1}]}
        must return on success: 27.48
        error_mode: raise

        precondition failure call (must raise HTTPException with a 4xx status): {"cart_items":[]}
    """
    if not cart_items:
        raise HTTPException(status_code=400, detail="Shopping cart contains at least one book")

    total_cost = 0.0
    for item in cart_items:
        total_cost += item["price"] * item["quantity"]

    return total_cost
