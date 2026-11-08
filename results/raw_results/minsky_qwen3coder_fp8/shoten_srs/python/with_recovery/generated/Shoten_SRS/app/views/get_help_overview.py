from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.with_recovery.generated.Shoten_SRS.app.extensions import Base, SessionLocal

class Operation(Base):
    __tablename__ = "operations"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

router = APIRouter()


def get_help_overview() -> dict[str, list[dict[str, str]]]:
    """System displays an overview of how to use the various operations defined above.

    Returns:
        A structured overview of all operations and their descriptions
    """
    # Return hardcoded overview as per requirement
    return {
        "operations": [
            {"name": "view_overview", "description": "Display help overview"},
            {"name": "select_operation", "description": "Select an operation by name"},
            {"name": "view_operation_details", "description": "View detailed info for a selected operation"}
        ]
    }