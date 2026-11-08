"""Stub models for entities imported across isolated FRs but defined in no file.

Generated mechanically by the packager so the assembled app boots; columns are
inferred from attribute usage, never from business logic."""
from sqlalchemy import Column, Integer, String

from app.extensions import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=True)
