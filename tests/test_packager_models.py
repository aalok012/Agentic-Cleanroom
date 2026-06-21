"""Packager model-collision repairs: differently-named classes mapping to the same table
(an isolated-generation artifact) must be unified into one bootable mapping."""

import subprocess
import sys
from pathlib import Path

from src.cleanroom.utils.packager import build_runnable_package

# Two FRs model the SAME 'dishes' table with different class names AND conflicting primary
# keys — the exact shape that crashed boot with "Trying to redefine primary-key column".
_VIEW = '''
from fastapi import APIRouter
from sqlalchemy import Column, Integer, String
from app.extensions import Base, SessionLocal

class DishModel(Base):
    __tablename__ = "dishes"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

router = APIRouter()

@router.post("")
def display_available_dishes() -> dict:
    db = SessionLocal()
    try:
        return {"dishes": [{"name": d.name, "quantity": d.quantity} for d in db.query(DishModel).all()]}
    finally:
        db.close()
'''

_MODEL = '''
from sqlalchemy import Column, String
from app.extensions import Base

class Dish(Base):
    __tablename__ = "dishes"
    name = Column(String, primary_key=True)
    classification = Column(String)
'''


def _sample() -> dict:
    return {"files": [
        {"fr_id": "1.1", "feature_id": "1", "path": "views/display_available_dishes.py",
         "mvc_layer": "view", "content": _VIEW},
        {"fr_id": "1.2", "feature_id": "1", "path": "models/assign_dish_to_chef.py",
         "mvc_layer": "model", "content": _MODEL},
    ]}


def test_conflicting_same_table_models_unify_and_boot(tmp_path: Path):
    out = tmp_path / "code"
    build_runnable_package(_sample(), out)

    # The canonical model carries the UNION of columns with a single `id` primary key.
    canon = (out / "app" / "models" / "assign_dish_to_chef.py").read_text()
    assert "id = Column(Integer, primary_key=True)" in canon
    assert "classification" in canon and "quantity" in canon
    # name is demoted from primary key on the unified model.
    assert "name = Column(String, primary_key=True)" not in canon

    # The other file aliases the canonical class instead of redefining the table.
    view = (out / "app" / "views" / "display_available_dishes.py").read_text()
    assert "from app.models.assign_dish_to_chef import Dish as DishModel" in view

    # The whole thing boots — no "redefine primary-key column" ArgumentError.
    boot = subprocess.run(
        [sys.executable, "-c",
         "from app import create_app; from fastapi.testclient import TestClient; "
         "TestClient(create_app()).post('/views/display_available_dishes')"],
        cwd=out, capture_output=True, text=True,
    )
    assert boot.returncode == 0, boot.stderr[-800:]
