"""Lay out generated Java sources so `javac` can compile them.

Each generated file's public class name is read from its content and written as `<Class>.java`
under `<code_dir>/src` (default package, flat) — javac requires the file name to match the public
class. v1 keeps features self-contained (no cross-class calls, no build system).
"""

from __future__ import annotations

import re
from pathlib import Path

_PUBLIC_CLASS = re.compile(r"public\s+(?:final\s+)?class\s+([A-Za-z_]\w*)")


def java_class_name(content: str, fallback: str) -> str:
    m = _PUBLIC_CLASS.search(content or "")
    return m.group(1) if m else fallback


def write_java_sources(generated_code: dict, code_dir: Path) -> list[Path]:
    """Write every Java file under code_dir/src as <PublicClass>.java. Returns the paths."""
    src = Path(code_dir) / "src"
    src.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    used: set[str] = set()
    for i, f in enumerate(generated_code.get("files", [])):
        content = f.get("content", "")
        fallback = "Gen" + re.sub(r"\W", "_", str(f.get("fr_id", i)))
        name = java_class_name(content, fallback)
        if name in used:                      # avoid clobbering on a duplicated class name
            name = f"{name}_{i}"
        used.add(name)
        dest = src / f"{name}.java"
        dest.write_text(content)
        written.append(dest)
    return written
