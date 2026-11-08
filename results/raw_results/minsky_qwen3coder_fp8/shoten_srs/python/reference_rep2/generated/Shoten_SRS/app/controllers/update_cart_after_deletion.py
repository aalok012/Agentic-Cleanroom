from fastapi import APIRouter, Body, HTTPException
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.reference_rep2.generated.Shoten_SRS.app.models._stubs import CartItem
from sqlalchemy import Column, Integer, String, Float

class CartItemModel(Base):
    __tablename__ = "cart_items"
    __table_args__ = {"extend_existing": True}
    user_id = Column(String)
    book_id = Column(String)
    title = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    id = Column(Integer, primary_key=True)

router = APIRouter()

@router.post("")
def update_cart_after_deletion(user_id: str = Body(..., embed=True), book_id: str = Body(..., embed=True)) -> list[dict[str, str]]:
    db = SessionLocal()
    try:
        # Check if user is registered and logged-in (basic check)
        if not user_id:
            raise HTTPException(status_code=403, detail="User is not registered or logged-in")
        
        # Check if the book exists in the user's cart
        cart_item = db.query(CartItemModel).filter(
            CartItemModel.user_id == user_id,
            CartItemModel.book_id == book_id
        ).first()
        
        if not cart_item:
            raise HTTPException(status_code=404, detail="Book not found in the user's shopping cart")
        
        # Remove the book from the cart
        db.delete(cart_item)
        db.commit()
        
        # Retrieve the updated cart
        updated_cart = db.query(CartItemModel).filter(
            CartItemModel.user_id == user_id
        ).all()
        
        # Format the response
        result = []
        for item in updated_cart:
            result.append({
                "id": item.book_id,
                "title": item.title
            })
        
        return result
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()