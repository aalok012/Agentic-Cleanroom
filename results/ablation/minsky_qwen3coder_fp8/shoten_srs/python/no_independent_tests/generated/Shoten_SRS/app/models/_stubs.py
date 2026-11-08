"""Stub models for entities imported across isolated FRs but defined in no file.

Generated mechanically by the packager so the assembled app boots; columns are
inferred from attribute usage, never from business logic."""
from sqlalchemy import Column, Integer, String

from results.ablation.minsky_qwen3coder_fp8.shoten_srs.python.no_independent_tests.generated.Shoten_SRS.app.extensions import Base


class Cart(Base):
    __tablename__ = "cart"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    book_id = Column(String, nullable=True)
    user_id = Column(String, nullable=True)


class Rental(Base):
    __tablename__ = "rental"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=True)
