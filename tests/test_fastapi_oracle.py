"""End-to-end check of the FastAPI certification path: assemble a synthetic generated
sample into a runnable app, then drive it through the HTTP oracle (TestClient subprocess)
for both the success (eq) and precondition-failure (raises) oracles."""

from pathlib import Path

from src.cleanroom.agents.evaluation.runner import route_from_file_path, run_case_http
from src.cleanroom.utils.packager import build_runnable_package

# A model + a controller that reads/writes the shared DB — the shape the FastAPI prompt
# mandates (Body params, @router.post(""), HTTPException on bad input, no hardcoded data).
_MODEL = '''
from sqlalchemy import Column, Integer, String
from app.extensions import Base


class Dish(Base):
    __tablename__ = "dishes"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    qty = Column(Integer)
'''

_CONTROLLER = '''
from fastapi import APIRouter, Body, HTTPException

from app.extensions import SessionLocal
from app.models.dish import Dish

router = APIRouter()


@router.post("")
def add_dish(name: str = Body(...), qty: int = Body(...)) -> dict:
    if qty < 0:
        raise HTTPException(status_code=400, detail="qty must be non-negative")
    db = SessionLocal()
    try:
        db.add(Dish(name=name, qty=qty))
        db.commit()
        return {"name": name, "qty": qty}
    finally:
        db.close()
'''


def _sample() -> dict:
    return {
        "files": [
            {"fr_id": "1.1", "feature_id": "1", "path": "models/dish.py",
             "mvc_layer": "model", "content": _MODEL},
            {"fr_id": "1.2", "feature_id": "1", "path": "controllers/add_dish.py",
             "mvc_layer": "controller", "content": _CONTROLLER},
        ]
    }


def test_route_derivation():
    assert route_from_file_path("controllers/add_dish.py") == "/controllers/add_dish"


def test_fastapi_oracle_success_and_failure(tmp_path: Path):
    out_dir = tmp_path / "code"
    build_runnable_package(_sample(), out_dir)

    ok, reason = run_case_http(
        out_dir, "controllers/add_dish.py",
        {"inputs_json": '{"name": "pasta", "qty": 2}',
         "expected_json": '{"name": "pasta", "qty": 2}', "oracle": "eq"},
    )
    assert ok, reason

    ok, reason = run_case_http(
        out_dir, "controllers/add_dish.py",
        {"inputs_json": '{"name": "x", "qty": -1}',
         "expected_json": '{"raises": "HTTPException"}', "oracle": "raises"},
    )
    assert ok, reason


def test_fastapi_oracle_detects_wrong_body(tmp_path: Path):
    out_dir = tmp_path / "code"
    build_runnable_package(_sample(), out_dir)
    ok, reason = run_case_http(
        out_dir, "controllers/add_dish.py",
        {"inputs_json": '{"name": "pasta", "qty": 2}',
         "expected_json": '{"name": "pasta", "qty": 99}', "oracle": "eq"},
    )
    assert not ok and "expected" in reason
