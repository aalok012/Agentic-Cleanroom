from fastapi import APIRouter, Body, HTTPException, status

router = APIRouter()

def display_order_shipping_details(order: dict[str, str]) -> dict[str, str]:
    # Validate precondition: order exists and user has access
    if not order or "shipping_date" not in order or "delivery_address" not in order or "projected_delivery_date" not in order or "status" not in order:
        raise HTTPException(status_code=400, detail="Order does not exist or user does not have access")
    
    # Extract required fields
    shipping_date = order.get("shipping_date")
    delivery_address = order.get("delivery_address")
    projected_delivery_date = order.get("projected_delivery_date")
    status = order.get("status")
    
    # Return formatted shipping details
    return {
        "shipping_date": shipping_date,
        "delivery_address": delivery_address,
        "projected_delivery_date": projected_delivery_date,
        "status": status
    }