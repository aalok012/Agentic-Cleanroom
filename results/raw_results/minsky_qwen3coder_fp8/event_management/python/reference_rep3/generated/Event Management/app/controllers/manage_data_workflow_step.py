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

router = APIRouter()

@router.post("")
def manage_data_workflow_step(action: str = Body(..., embed=True), data: dict = Body(..., embed=True)) -> dict:
    db = SessionLocal()
    try:
        if action == "enter":
            # Create a new data entry
            entry = DataEntry(title=data.get("title"), content=data.get("content"))
            db.add(entry)
            db.commit()
            db.refresh(entry)
            return {"next_step": "organize", "message": "Data entered successfully. Proceed to organize the data."}
        
        elif action == "organize":
            # For now, we'll just return a success message
            return {"next_step": "retrieve", "message": "Data organized successfully. Proceed to retrieve the data."}
        
        elif action == "retrieve":
            # Retrieve data based on provided ID
            entry_id = data.get("id")
            if not entry_id:
                raise HTTPException(status_code=400, detail="ID is required for retrieval.")
            
            entry = db.query(DataEntry).filter(DataEntry.id == entry_id).first()
            if not entry:
                raise HTTPException(status_code=404, detail="Data entry not found.")
            
            return {"next_step": "modify", "data": {"id": entry.id, "title": entry.title, "content": entry.content}, "message": "Data retrieved successfully. Proceed to modify the data."}
        
        elif action == "modify":
            # Modify existing data
            entry_id = data.get("id")
            if not entry_id:
                raise HTTPException(status_code=400, detail="ID is required for modification.")
            
            entry = db.query(DataEntry).filter(DataEntry.id == entry_id).first()
            if not entry:
                raise HTTPException(status_code=404, detail="Data entry not found.")
            
            # Update fields if provided
            if "title" in data:
                entry.title = data["title"]
            if "content" in data:
                entry.content = data["content"]
            
            db.commit()
            db.refresh(entry)
            return {"next_step": "delete", "message": "Data modified successfully. Proceed to delete the data."}
        
        elif action == "delete":
            # Delete data
            entry_id = data.get("id")
            if not entry_id:
                raise HTTPException(status_code=400, detail="ID is required for deletion.")
            
            entry = db.query(DataEntry).filter(DataEntry.id == entry_id).first()
            if not entry:
                raise HTTPException(status_code=404, detail="Data entry not found.")
            
            db.delete(entry)
            db.commit()
            return {"next_step": "enter", "message": "Data deleted successfully. Start a new entry."}
        
        else:
            raise HTTPException(status_code=400, detail="Invalid action. Must be 'enter', 'organize', 'retrieve', 'modify', or 'delete'.")
    finally:
        db.close()