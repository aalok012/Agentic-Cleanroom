from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import Session
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base, SessionLocal
from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.models._stubs import CartItem

class CartItemModel(Base):
    __tablename__ = "cart_items"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    quantity = Column(Integer)
    price = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))

router = APIRouter()

@router.post("")
def fr_4_4_REQ_2(request: dict = Body(..., embed=True)) -> dict:
    db = SessionLocal()
    try:
        cart_items = db.query(CartItemModel).all()
        total_price = sum(item.price * item.quantity for item in cart_items)
        return {"total_price": total_price}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()