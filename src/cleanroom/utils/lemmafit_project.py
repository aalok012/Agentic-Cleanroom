"""Scaffold a LemmaFit project and compile verified Dafny to TypeScript.

The packager for the LemmaFit/TypeScript stack: ``scaffold_lemmafit_project`` runs
``lemmafit init`` (which lays down ``Replay.dfy`` + the ``.claude/skills`` the DafnyAgent reads
and verifies against), and ``compile_dafny_to_ts`` turns each verified feature module into a
TypeScript client via the bundled ``dafny2js`` (appending a standard ``AppCore`` wrapper, which
dafny2js needs to detect the app surface). Compilation is best-effort — the verified Dafny is the
primary, formally-guaranteed artifact; TS emission is a convenience on top.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from src.cleanroom.agents.dafny.schema.dafny import GeneratedDafny
from src.cleanroom.utils.dafny_verify import dafny_binary

_DAFNY2JS = Path.home() / ".lemmafit" / ".dafny2js" / "dafny2js"

# Standard AppCore wrapper over a feature's Kernel — pure boilerplate (no new proof obligations)
# that exposes the app surface dafny2js compiles to a TS client.
_APPCORE = """

module AppCore {{
  import K = {mod}Kernel
  import D = {mod}Domain
  function Init(): K.History {{ K.InitHistory() }}
  function Dispatch(h: K.History, a: D.Action): K.History
    requires D.Inv(h.present)
  {{ K.Do(h, a) }}
  function Present(h: K.History): D.Model {{ h.present }}
  function Undo(h: K.History): K.History {{ K.Undo(h) }}
  function Redo(h: K.History): K.History {{ K.Redo(h) }}
}}
"""


def lemmafit_available() -> bool:
    return shutil.which("lemmafit") is not None


def scaffold_lemmafit_project(project_dir: Path, install_deps: bool = True) -> Path:
    """Create a fresh LemmaFit project at ``project_dir`` (Replay.dfy + skills + scaffolding).

    With ``install_deps`` (default), also runs ``npm install`` so the generated project is
    directly runnable (``npm run dev``) — best-effort: a failure is logged but does not abort,
    since Dafny verification and the Dafny→TS compile use the global toolchain, not node_modules.
    """
    if shutil.which("lemmafit") is None:
        raise RuntimeError("lemmafit CLI not found — run: npm install -g lemmafit")
    if project_dir.exists():
        shutil.rmtree(project_dir)
    project_dir.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["lemmafit", "init", str(project_dir)], check=True, capture_output=True, text=True)

    if install_deps and shutil.which("npm") is not None:
        proc = subprocess.run(["npm", "install"], cwd=str(project_dir),
                              capture_output=True, text=True, timeout=600)
        if proc.returncode != 0:
            print(f"  (npm install failed — project still verifies; run it manually to run the app: "
                  f"{(proc.stderr or proc.stdout).strip()[:160]})")
    return project_dir


def compile_dafny_to_ts(project_dir: Path, gen: GeneratedDafny, timeout: float = 240.0) -> dict:
    """Compile each VERIFIED feature module to a RUNNABLE TS client (best-effort).

    Mirrors the LemmaFit daemon's three-step chain so the output is actually runnable:
      1. ``dafny translate js`` → a self-contained ``.js`` of the verified logic;
      2. copy it to ``src/dafny/<module>.cjs`` (the bundle the adapter imports);
      3. ``dafny2js --client`` → ``src/dafny/<module>.ts`` (the typed adapter that imports the .cjs).
    """
    dafny = dafny_binary()
    if dafny is None or not _DAFNY2JS.exists():
        return {"compiled": [], "failed": [], "note": "dafny / dafny2js not found; skipped"}

    project_dir = project_dir.resolve()      # the tools need absolute paths
    out_dir = project_dir / "src" / "dafny"
    gen_dir = project_dir / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    gen_dir.mkdir(parents=True, exist_ok=True)
    dafny_dir = project_dir / "lemmafit" / "dafny"
    compiled: list[dict] = []
    failed: list[dict] = []

    def _run(cmd):
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=str(project_dir))

    for f in gen.features:
        if not f.verified:
            failed.append({"feature_id": f.feature_id, "reason": "dafny not verified"})
            continue
        src = (dafny_dir / f"{f.module}.dfy").resolve()
        if not src.exists():
            failed.append({"feature_id": f.feature_id, "reason": "missing .dfy"})
            continue
        text = src.read_text()
        if "module AppCore" not in text:
            src.write_text(text + _APPCORE.format(mod=f.module))

        out_base = (gen_dir / f.module).resolve()
        cjs = (out_dir / f"{f.module}.cjs").resolve()
        out_ts = (out_dir / f"{f.module}.ts").resolve()
        try:
            # 1. Dafny → JS (self-contained, skip re-verification — already proven).
            #    --allow-warnings: style warnings must not fail translation of verified code.
            tr = _run([dafny, "translate", "js", "--no-verify", "--allow-warnings",
                       "-o", str(out_base), "--include-runtime", str(src)])
            if not (gen_dir / f"{f.module}.js").exists():
                failed.append({"feature_id": f.feature_id,
                               "reason": ("dafny translate: " + (tr.stderr or tr.stdout)).strip()[:160]})
                continue
            # 2. Place the bundle next to the adapter.
            shutil.copyfile(gen_dir / f"{f.module}.js", cjs)
            # 3. Generate the typed client adapter that imports the .cjs.
            d2 = _run([str(_DAFNY2JS), "--file", str(src), "--app-core", "AppCore",
                       "--cjs-name", f"{f.module}.cjs", "--client", str(out_ts)])
        except (OSError, subprocess.SubprocessError) as exc:
            failed.append({"feature_id": f.feature_id, "reason": str(exc)[:160]})
            continue
        if d2.returncode == 0 and out_ts.exists() and cjs.exists():
            compiled.append({"feature_id": f.feature_id, "ts": str(out_ts), "cjs": str(cjs)})
        else:
            failed.append({"feature_id": f.feature_id,
                           "reason": ("dafny2js: " + (d2.stderr or d2.stdout or "failed")).strip()[:160]})
    return {"compiled": compiled, "failed": failed}
