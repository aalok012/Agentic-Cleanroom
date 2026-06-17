"""Turn generated MVC code into an importable, runnable Python package.

The Code Agent emits each increment in isolation, so intra-project imports don't
agree on a layout (e.g. ``from models.health_event import X`` while the file lives
at ``model/health_event.py``). This post-step assembles the files into one ``app``
package, rewrites intra-project imports to match, adds ``__init__.py`` files, and
writes a ``main.py`` that imports every module so you can verify the package wires
up.

It is MECHANICAL only — it changes import statements and file layout, never program
logic — so the no-feedback isolation of the pipeline is not affected.
"""

import ast
from pathlib import Path

_MAIN_TEMPLATE = '''"""Smoke driver: import every generated module and report what loaded.

Run from this directory:  python -m app.main
(Some View modules need third-party libs — see ../requirements.txt.)
"""
import importlib
import pkgutil


def main() -> None:
    ok, failed = [], []
    for layer in ("model", "controller", "view"):
        try:
            pkg = importlib.import_module(f"app.{layer}")
        except ModuleNotFoundError:
            continue
        for info in pkgutil.iter_modules(pkg.__path__):
            name = f"app.{layer}.{info.name}"
            try:
                module = importlib.import_module(name)
                classes = [n for n in vars(module) if n[:1].isupper()]
                ok.append((name, classes))
            except Exception as exc:  # noqa: BLE001 - report, don't crash
                failed.append((name, f"{type(exc).__name__}: {exc}"))

    print(f"Imported {len(ok)} module(s):")
    for name, classes in ok:
        print(f"  {name}: {', '.join(classes) or '(no top-level classes)'}")
    if failed:
        print(f"\\n{len(failed)} module(s) need attention (often a missing dependency):")
        for name, err in failed:
            print(f"  {name}: {err}")


if __name__ == "__main__":
    main()
'''


def _collect(generated_code: dict) -> list[tuple[str, str, str]]:
    """[(layer, filename, content)], de-duplicating same-named files within a layer."""
    out: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()
    for inc in generated_code.get("increments", []):
        for f in inc.get("files", []):
            layer = (f.get("mvc_layer") or "unknown").strip().lower() or "unknown"
            name = Path(f["path"]).name
            if (layer, name) in seen:
                name = f"{Path(name).stem}_inc{inc.get('increment_id', 'x')}{Path(name).suffix}"
            seen.add((layer, name))
            out.append((layer, name, f.get("content", "")))
    return out


def _rewrite_imports(content: str, stem_to_layer: dict[str, str]) -> str:
    """Rewrite intra-project imports to absolute ``app.<layer>.<module>`` paths."""
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return content  # leave unparseable generated files untouched

    lines = content.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            last = node.module.split(".")[-1]
            layer = stem_to_layer.get(last)
            if layer:
                i = node.lineno - 1
                lines[i] = lines[i].replace(f"from {node.module} import", f"from app.{layer}.{last} import", 1)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                last = alias.name.split(".")[-1]
                layer = stem_to_layer.get(last)
                if layer and alias.name != last:  # only dotted intra-project imports
                    i = node.lineno - 1
                    lines[i] = lines[i].replace(f"import {alias.name}", f"import app.{layer}.{last} as {last}", 1)

    trailing = "\n" if content.endswith("\n") else ""
    return "\n".join(lines) + trailing


def build_runnable_package(generated_code: dict, out_dir: Path) -> Path:
    """Assemble generated_code into out_dir/app/ as an importable package. Returns the app dir."""
    from src.cleanroom.utils.code_stats import code_stats

    files = _collect(generated_code)
    stem_to_layer = {Path(name).stem: layer for layer, name, _ in files}

    app = out_dir / "app"
    app.mkdir(parents=True, exist_ok=True)
    (app / "__init__.py").write_text("")

    layers: set[str] = set()
    for layer, name, content in files:
        layers.add(layer)
        dest = app / layer / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(_rewrite_imports(content, stem_to_layer))
    for layer in layers:
        (app / layer / "__init__.py").write_text("")

    (app / "main.py").write_text(_MAIN_TEMPLATE)

    third_party = code_stats(generated_code)["third_party_libraries"]
    (out_dir / "requirements.txt").write_text("\n".join(third_party) + ("\n" if third_party else ""))
    return app


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) != 2:
        print("usage: python -m src.cleanroom.utils.packager <full_ir.json>")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as fh:
        ir = json.load(fh)
    if "generated_code" not in ir:
        print("IR has no 'generated_code' — run the pipeline (with the LLM stages) first.")
        sys.exit(1)

    out = Path("outputs/generated") / ir.get("project_name", "project") / "runnable"
    app_dir = build_runnable_package(ir["generated_code"], out)
    print(f"Runnable package written to: {app_dir}")
    print("Run it with:")
    print(f'  cd "{out}"')
    print("  python -m app.main")
