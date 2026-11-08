from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import Session
from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal


from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.models.store_user_information import User


router = APIRouter()


def generate_username(name: str, user_type: str, roll_number: str, shop_id: str) -> str:
    # Generate a basic username from the name
    base_username = "".join(name.lower().split())
    
    # Add a suffix based on user type
    if user_type == "student":
        suffix = roll_number[-3:] if roll_number else "std"
    elif user_type == "bookstore":
        suffix = shop_id[-3:] if shop_id else "bsk"
    else:
        suffix = "gen"
    
    return f"{base_username}{suffix}"


@router.post("")
def assign_username_and_prompt_password(
    name: str = Body(..., embed=True),
    user_type: str = Body(..., embed=True),
    roll_number: str = Body(..., embed=True),
    shop_id: str = Body(..., embed=True),
    mobile_number: str = Body(..., embed=True),
    email_id: str = Body(..., embed=True)
) -> dict[str, str]:
    # Check preconditions
    if not name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    # Validate user type
    valid_user_types = ["student", "bookstore", "general"]
    if user_type not in valid_user_types:
        raise HTTPException(status_code=400, detail="Invalid user type")
    
    # Validate required fields
    if user_type == "student" and not roll_number:
        raise HTTPException(status_code=400, detail="Roll number is required for students")
    
    if user_type == "bookstore" and not shop_id:
        raise HTTPException(status_code=400, detail="Shop ID is required for bookstores")
    
    db = SessionLocal()
    try:
        # Generate username
        username = generate_username(name, user_type, roll_number, shop_id)
        
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            # Append a number to make it unique
            counter = 1
            while True:
                new_username = f"{username}{counter}"
                if not db.query(User).filter(User.username == new_username).first():
                    username = new_username
                    break
                counter += 1
        
        # Create a new user entry
        new_user = User(
            name=name,
            username=username,
            user_type=user_type,
            roll_number=roll_number,
            shop_id=shop_id,
            mobile_number=mobile_number,
            email_id=email_id
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {"username": username, "prompt": "Please set a password"}
    finally:
        db.close()