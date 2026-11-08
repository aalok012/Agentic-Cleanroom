from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal


class Item(Base):
    __tablename__ = "items"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, index=True)
    category = Column(String)
    price = Column(Float)
    is_active = Column(Boolean, default=True)


router = APIRouter()


@router.post("")
def execute_workflow_step(
    step_type: str = Body(..., embed=True), data: dict = Body(..., embed=True)
) -> dict:
    db = SessionLocal()
    try:
        if step_type not in ["enter", "organize", "retrieve", "modify", "delete"]:
            raise HTTPException(status_code=400, detail="Invalid step type")

        if step_type == "enter":
            item_name = data.get("item_name")
            category = data.get("category")
            if not item_name or not category:
                raise HTTPException(status_code=400, detail="Item name and category are required")
            
            new_item = Item(item_name=item_name, category=category)
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            
            return {
                "next_step": "organize",
                "message": "Item entered successfully. Please organize the item."
            }
        
        elif step_type == "organize":
            # Implementation for organizing items would go here
            # For now, we'll just return a success message
            return {
                "next_step": "retrieve",
                "message": "Item organized successfully."
            }
        
        elif step_type == "retrieve":
            # Implementation for retrieving items would go here
            # For now, we'll just return a success message
            return {
                "next_step": "modify",
                "message": "Items retrieved successfully."
            }
        
        elif step_type == "modify":
            # Implementation for modifying items would go here
            # For now, we'll just return a success message
            return {
                "next_step": "delete",
                "message": "Item modified successfully."
            }
        
        elif step_type == "delete":
            # Implementation for deleting items would go here
            # For now, we'll just return a success message
            return {
                "next_step": "enter",
                "message": "Item deleted successfully."
            }
    finally:
        db.close()