from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal


class DataEntry(Base):
    __tablename__ = "data_entries"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    category = Column(String)


router = APIRouter()


@router.post("")
def manage_data_workflow_step(
    action: str = Body(..., embed=True), data: dict = Body(..., embed=True)
) -> dict:
    db = SessionLocal()
    try:
        if action == "enter":
            # Create a new data entry
            entry = DataEntry(
                title=data.get("title"),
                content=data.get("content"),
                category=None  # Will be set during organize step
            )
            db.add(entry)
            db.commit()
            db.refresh(entry)
            return {
                "next_step": "organize",
                "instructions": "Please organize the entered data by category"
            }
        elif action == "organize":
            # Update the entry with category
            entry_id = data.get("id")
            category = data.get("category")
            entry = db.query(DataEntry).filter(DataEntry.id == entry_id).first()
            if not entry:
                raise HTTPException(status_code=404, detail="Data entry not found")
            entry.category = category
            db.commit()
            db.refresh(entry)
            return {
                "next_step": "retrieve",
                "instructions": "Data organized successfully. You can now retrieve it."
            }
        elif action == "retrieve":
            # Retrieve data based on provided criteria
            entry_id = data.get("id")
            entry = db.query(DataEntry).filter(DataEntry.id == entry_id).first()
            if not entry:
                raise HTTPException(status_code=404, detail="Data entry not found")
            return {
                "next_step": "modify",
                "data": {
                    "id": entry.id,
                    "title": entry.title,
                    "content": entry.content,
                    "category": entry.category
                },
                "instructions": "Modify the retrieved data as needed"
            }
        elif action == "modify":
            # Modify existing data
            entry_id = data.get("id")
            entry = db.query(DataEntry).filter(DataEntry.id == entry_id).first()
            if not entry:
                raise HTTPException(status_code=404, detail="Data entry not found")
            
            # Update fields if provided
            if "title" in data:
                entry.title = data["title"]
            if "content" in data:
                entry.content = data["content"]
            if "category" in data:
                entry.category = data["category"]
            
            db.commit()
            db.refresh(entry)
            return {
                "next_step": "delete",
                "instructions": "Data modified successfully. You can now delete it if needed."
            }
        elif action == "delete":
            # Delete data
            entry_id = data.get("id")
            entry = db.query(DataEntry).filter(DataEntry.id == entry_id).first()
            if not entry:
                raise HTTPException(status_code=404, detail="Data entry not found")
            db.delete(entry)
            db.commit()
            return {
                "next_step": "complete",
                "instructions": "Data deleted successfully. Workflow completed."
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
    finally:
        db.close()