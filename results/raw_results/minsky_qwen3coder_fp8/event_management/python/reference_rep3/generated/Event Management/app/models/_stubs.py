"""Stub models for entities imported across isolated FRs but defined in no file.

Generated mechanically by the packager so the assembled app boots; columns are
inferred from attribute usage, never from business logic."""
from sqlalchemy import Column, Integer, String

from app.extensions import Base


class Client(Base):
    __tablename__ = "client"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    client_id = Column(String, nullable=True)


class Registration(Base):
    __tablename__ = "registration"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=True)
