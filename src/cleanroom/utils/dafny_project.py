"""Scaffold a Dafny verification project and compile verified Dafny to native code.

No npm / external toolchain dependency: ``scaffold_dafny_project`` just makes a directory and drops
in our vendored ``Replay.dfy`` kernel (the abstract Domain/Kernel that feature modules refine).
``compile_dafny`` turns each VERIFIED feature module into native source via the stock
``dafny translate <target>`` backend (default Python). Compilation is best-effort — the verified
Dafny is the primary, formally-guaranteed artifact; native emission is a convenience on top.

Project layout:
    <project_dir>/
      dafny/   Replay.dfy (vendored)  +  F<feat>.dfy (generated, one per feature)
      out/     dafny translate output for the verified modules
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from src.cleanroom.agents.dafny.schema.dafny import GeneratedDafny
from src.cleanroom.utils.dafny_verify import dafny_binary

# Our vendored kernel, owned in-repo (no external install needed).
KERNEL_SRC = Path(__file__).resolve().parents[1] / "agents" / "dafny" / "kernel" / "Replay.dfy"


def scaffold_dafny_project(project_dir: Path) -> Path:
    """Create a fresh Dafny project at ``project_dir``: a ``dafny/`` dir + the vendored kernel.

    Verification and ``dafny translate`` use only the ``dafny`` binary, so no node project is needed.
    """
    project_dir = Path(project_dir)
    if project_dir.exists():
        shutil.rmtree(project_dir)
    dafny_dir = project_dir / "dafny"
    dafny_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(KERNEL_SRC, dafny_dir / "Replay.dfy")
    return project_dir


def stage_dafny_cores(app_dir: Path, project_dir: Path, modules: list[str]) -> dict:
    """Copy compiled cores + the marshalling shim into a runnable app under ``app_dir/dafny_cores``.

    For each proved feature ``module`` (e.g. ``F4_1``) the compiled ``out/<module>-py/`` dir is
    copied to ``app_dir/dafny_cores/<module>-py/`` (it bundles its own ``_dafny`` runtime), and the
    shared ``dafny_marshal.py`` shim lands at ``app_dir/dafny_cores/dafny_marshal.py``. The generated
    adapters discover this dir by searching upward for ``dafny_cores`` (see generate_adapter.j2).
    """
    app_dir, project_dir = Path(app_dir), Path(project_dir)
    cores_dir = app_dir / "dafny_cores"
    cores_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__).resolve().parent / "dafny_marshal.py", cores_dir / "dafny_marshal.py")
    staged, missing = [], []
    for module in modules:
        src = project_dir / "out" / f"{module}-py"
        if not src.is_dir():
            missing.append(module)
            continue
        dst = cores_dir / f"{module}-py"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        staged.append(module)
    return {"cores_dir": str(cores_dir), "staged": staged, "missing": missing}


def stage_dafny_cores_java(maven_dir: Path, project_dir: Path, modules: list[str]) -> dict:
    """Copy translated Dafny Java cores into a Maven project's ``src/main/java`` so it compiles.

    For each proved feature ``module`` (e.g. ``F4_1``) ``dafny translate java --include-runtime``
    produced ``out/<module>-java/`` — a package tree of ``.java`` sources that bundles its OWN copy
    of the ``dafny`` runtime. We replicate each file at its package-relative path under
    ``src/main/java``, but SKIP a destination that already exists: that dedupes the shared
    ``dafny`` runtime across multiple staged cores (first writer wins — every core bundles the same
    runtime), so javac never sees a duplicate class. Returns staged/missing module lists.
    """
    src_root = Path(maven_dir) / "src" / "main" / "java"
    src_root.mkdir(parents=True, exist_ok=True)
    staged, missing = [], []
    for module in modules:
        core_dir = Path(project_dir) / "out" / f"{module}-java"
        if not core_dir.is_dir():
            missing.append(module)
            continue
        for jf in core_dir.rglob("*.java"):
            dst = src_root / jf.relative_to(core_dir)
            if dst.exists():          # shared DafnyRuntime already staged by an earlier core
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(jf, dst)
        staged.append(module)
    return {"java_src": str(src_root), "staged": staged, "missing": missing}


def compile_dafny(project_dir: Path, gen: GeneratedDafny, target: str = "py",
                  timeout: float = 240.0) -> dict:
    """Compile each VERIFIED feature module to native source via ``dafny translate`` (best-effort).

    ``target`` is any stock Dafny backend: py | cs | js | go | java | cpp | rs. Returns
    {"target", "compiled": [...], "failed": [...]}. Unverified modules are skipped (a feature
    only compiles from a discharged proof — never from unproved code).
    """
    dafny = dafny_binary()
    if dafny is None:
        return {"target": target, "compiled": [], "failed": [],
                "note": "dafny binary not found; skipped"}

    project_dir = Path(project_dir).resolve()
    dafny_dir = project_dir / "dafny"
    out_dir = project_dir / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    compiled: list[dict] = []
    failed: list[dict] = []

    for f in gen.features:
        if not f.verified:
            failed.append({"feature_id": f.feature_id, "reason": "dafny not verified"})
            continue
        src = (dafny_dir / f"{f.module}.dfy").resolve()
        if not src.exists():
            failed.append({"feature_id": f.feature_id, "reason": "missing .dfy"})
            continue
        out_base = (out_dir / f.module).resolve()
        try:
            # --no-verify: already proved.  --allow-warnings: Dafny exits non-zero on STYLE
            # warnings even when translation succeeds, so we must not let those fail it.
            proc = subprocess.run(
                [dafny, "translate", target, "--no-verify", "--allow-warnings",
                 "--include-runtime", "-o", str(out_base), str(src)],
                capture_output=True, text=True, timeout=timeout, cwd=str(project_dir),
            )
        except (OSError, subprocess.SubprocessError) as exc:
            failed.append({"feature_id": f.feature_id, "reason": str(exc)[:160]})
            continue
        # dafny writes either <base>.<ext> or a <base>-<target>/ directory depending on backend.
        produced = sorted(p for p in out_dir.glob(f"{f.module}*") if p != src)
        if proc.returncode == 0 and produced:
            compiled.append({"feature_id": f.feature_id, "target": target,
                             "output": str(produced[0])})
        else:
            failed.append({"feature_id": f.feature_id,
                           "reason": ("dafny translate: " + (proc.stderr or proc.stdout or "failed")).strip()[:160]})
    return {"target": target, "compiled": compiled, "failed": failed}
