from fastapi import APIRouter, Body, HTTPException

router = APIRouter()

@router.post("")
def display_purchased_books(purchased_items: list[dict[str, object]] = Body(..., embed=True)) -> list[dict[str, object]]:
    if not purchased_items:
        raise HTTPException(status_code=400, detail="No purchased items provided")

    # Validate each item has required fields
    for item in purchased_items:
        if not all(key in item for key in ["title", "price", "quantity"]):
            raise HTTPException(status_code=400, detail="Each item must have title, price, and quantity")

    # Return the purchased items as-is since they already contain the required information
    return purchased_items
