from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from app.extensions import Base, SessionLocal

class ClientAccess(Base):
    __tablename__ = "client_access"
    __table_args__ = {"extend_existing": True}
    client_id = Column(String, primary_key=True)
    access_granted = Column(Boolean, default=True)

router = APIRouter()

@router.post("")
def manage_client_access(action: str = Body(..., embed=True), client_id: str = Body(..., embed=True)) -> dict[str, str]:
    db = SessionLocal()
    try:
        if action not in ["add", "delete"]:
            raise HTTPException(status_code=400, detail="Invalid action. Action must be either 'add' or 'delete'")
        
        client = db.query(ClientAccess).filter(ClientAccess.client_id == client_id).first()
        
        if action == "add":
            if client is None:
                new_client = ClientAccess(client_id=client_id)
                db.add(new_client)
            else:
                client.access_granted = True
        elif action == "delete":
            if client is None:
                raise HTTPException(status_code=404, detail="Client not found")
            client.access_granted = False
        
        db.commit()
        return {"status": "success", "message": "Client access " + action + "ed successfully"}
    finally:
        db.close()