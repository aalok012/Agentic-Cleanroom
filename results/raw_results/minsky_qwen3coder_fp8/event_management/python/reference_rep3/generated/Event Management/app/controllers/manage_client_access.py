from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal

class ClientAccess(Base):
    __tablename__ = "client_access"
    __table_args__ = {"extend_existing": True}
    client_id = Column(String, primary_key=True)
    permissions = Column(String, nullable=False)

router = APIRouter()

@router.post("")
def manage_client_access(client_id: str = Body(..., embed=True), permissions: list[str] = Body(..., embed=True), action: str = Body(..., embed=True)) -> dict[str, str]:
    # Validate inputs
    if not client_id:
        raise HTTPException(status_code=400, detail="Client ID cannot be empty.")
    
    if not permissions:
        raise HTTPException(status_code=400, detail="Permissions list cannot be empty.")
    
    if action not in ["add", "delete"]:
        raise HTTPException(status_code=400, detail="Action must be either 'add' or 'delete'.")
    
    db = SessionLocal()
    try:
        # Check if client exists
        existing_client = db.query(ClientAccess).filter(ClientAccess.client_id == client_id).first()
        
        if action == "add":
            if existing_client:
                raise HTTPException(status_code=400, detail="Client already has access.")
            
            # Create new client access
            new_client = ClientAccess(client_id=client_id, permissions=", ".join(permissions))
            db.add(new_client)
            db.commit()
            db.refresh(new_client)
            
            return {"status": "success", "message": "Client access added successfully."}
        
        elif action == "delete":
            if not existing_client:
                raise HTTPException(status_code=404, detail="Client access not found.")
            
            # Delete client access
            db.delete(existing_client)
            db.commit()
            
            return {"status": "success", "message": "Client access deleted successfully."}
    finally:
        db.close()