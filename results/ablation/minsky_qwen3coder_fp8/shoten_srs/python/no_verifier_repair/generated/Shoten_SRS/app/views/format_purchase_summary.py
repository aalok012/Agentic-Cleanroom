from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.extensions import Base, SessionLocal

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_verifier_repair.generated.Shoten_SRS.app.models.get_user_purchase_history import Purchase

router = APIRouter()


def format_purchase_summary(purchase: dict[str, object]) -> dict[str, object]:
    """For each purchase, the system displays the date of purchase and the payment mode used.

    Args:
        purchase: A single purchase record containing at least date and payment_mode fields

    Returns:
        Formatted dictionary with only date of purchase and payment mode

    Notes:
        Postcondition: Each displayed purchase includes both the date of purchase and the payment mode, and nothing else
        Prerequisite: get_user_purchase_history (req 4.13.REQ-1) must have run first.
        canonical call (must work): {"purchase":{"date":"2023-01-15","payment_mode":"credit_card"}}
        must return on success: {"date": "2023-01-15", "payment_mode": "credit_card"}
        error_mode: raise

        precondition failure call (must raise HTTPException with a 4xx status): {"purchase":{}}
    """
    # Validate that required fields exist
    if "date" not in purchase or "payment_mode" not in purchase:
        raise HTTPException(status_code=400, detail="Missing required fields: date or payment_mode")

    # Return only the required fields
    return {
        "date": purchase["date"],
        "payment_mode": purchase["payment_mode"]
    }
