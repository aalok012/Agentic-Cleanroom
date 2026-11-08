"""Stub models for entities imported across isolated FRs but defined in no file.

Generated mechanically by the packager so the assembled app boots; columns are
inferred from attribute usage, never from business logic."""
from sqlalchemy import Column, Integer, String

from results.raw_results.minsky_qwen3coder_fp8.shoten_srs.python.raw_spec_only.generated.Shoten_SRS.app.extensions import Base


class Cart(Base):
    __tablename__ = "cart"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)


class CartItem(Base):
    __tablename__ = "cartitem"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)


class Purchase(Base):
    __tablename__ = "purchase"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)


class Shipment(Base):
    __tablename__ = "shipment"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)


class Wishlist(Base):
    __tablename__ = "wishlist"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
