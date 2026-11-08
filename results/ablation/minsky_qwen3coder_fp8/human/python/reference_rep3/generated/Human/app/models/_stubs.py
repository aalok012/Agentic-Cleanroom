"""Stub models for entities imported across isolated FRs but defined in no file.

Generated mechanically by the packager so the assembled app boots; columns are
inferred from attribute usage, never from business logic."""
from sqlalchemy import Column, Integer, String

from results.ablation.minsky_qwen3coder_fp8.human.python.reference_rep3.generated.Human.app.extensions import Base


class Event(Base):
    __tablename__ = "event"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
