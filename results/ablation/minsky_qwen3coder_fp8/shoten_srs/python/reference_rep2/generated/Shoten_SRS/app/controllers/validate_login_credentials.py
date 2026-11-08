from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal


from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.models.store_user_information import User


router = APIRouter()


@router.post("")
def validate_login_credentials(username: str = Body(..., embed=True), password: str = Body(..., embed=True)) -> bool:
    """
    The system requires both a username and a password from the user before proceeding.

    Args:
        username: The username provided by the user for login.
        password: The password provided by the user for login.

    Returns:
        True if both username and password are provided, False otherwise.

    Notes:
        Postcondition: The system will not accept login without both required fields provided.
        canonical call (must work): {"username":"johndoe","password":"secret123"}
        must return on success: true
        error_mode: raise

        precondition failure call (must raise HTTPException with a 4xx status): {"username":"","password":"secret123"}
    """
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required.")
    
    db = SessionLocal()
    try:
        # Check if user exists in the database
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found.")
        
        # Validate password (in a real app, you'd hash and compare)
        if user.password != password:
            raise HTTPException(status_code=403, detail="Incorrect password.")
        
        return True
    finally:
        db.close()