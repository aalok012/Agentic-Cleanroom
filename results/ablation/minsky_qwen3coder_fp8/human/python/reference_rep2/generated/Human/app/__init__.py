"""Application factory: build the FastAPI app, init the database, register routers.

Generated mechanically by the pipeline's packager — no business logic lives here.
Run with:  uvicorn app:create_app --factory   (or: python -m app)
"""
import importlib
import pkgutil

from fastapi import APIRouter, FastAPI

from results.ablation.minsky_qwen3coder_fp8.human.python.reference_rep2.generated.Human.app.extensions import Base, engine

_LAYERS = ("models", "controllers", "views")


def create_app() -> FastAPI:
    app = FastAPI()

    # Import every generated module so models register on the metadata and routers
    # become importable, then register any APIRouter instances found. Each file is
    # generated in isolation, so router tags collide; register every distinct router
    # exactly once under a prefix made unique by its source module.
    registered_ids: set[int] = set()
    for layer in _LAYERS:
        try:
            package = importlib.import_module(f"app.{layer}")
        except ModuleNotFoundError:
            continue
        for info in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f"app.{layer}.{info.name}")
            for value in vars(module).values():
                if not isinstance(value, APIRouter) or id(value) in registered_ids:
                    continue
                registered_ids.add(id(value))
                prefix = f"/{layer}/{info.name}"
                app.include_router(value, prefix=prefix, tags=[info.name])

    Base.metadata.create_all(bind=engine)
    return app
