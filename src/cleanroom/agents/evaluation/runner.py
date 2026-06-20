"""Execute spec-derived test cases against generated code in an isolated subprocess."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path

_RUNNER_SCRIPT = textwrap.dedent(
    '''
    import importlib.util
    import json
    import sys
    from pathlib import Path

    code_root = Path(sys.argv[1])
    file_path = sys.argv[2]
    func_name = sys.argv[3]
    inputs_json = sys.argv[4]
    expected_json = sys.argv[5]
    oracle = sys.argv[6]

    sys.path.insert(0, str(code_root))
    module_path = code_root / file_path
    spec = importlib.util.spec_from_file_location("candidate_mod", module_path)
    if spec is None or spec.loader is None:
        print(json.dumps({"pass": False, "reason": f"cannot load {file_path}"}))
        raise SystemExit(0)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, func_name, None)
    if fn is None:
        print(json.dumps({"pass": False, "reason": f"function {func_name} not found in {file_path}"}))
        raise SystemExit(0)

    inputs = json.loads(inputs_json)

    def normalize(value):
        if isinstance(value, dict):
            return {str(k): normalize(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [normalize(v) for v in value]
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        if hasattr(value, "__dict__"):
            return normalize(vars(value))
        return str(value)

    try:
        if oracle == "raises":
            expected = json.loads(expected_json)
            exc_name = expected.get("raises", "ValueError")
            try:
                fn(**inputs)
                print(json.dumps({"pass": False, "reason": f"expected {exc_name} but no exception raised"}))
            except Exception as exc:
                ok = type(exc).__name__ == exc_name
                reason = type(exc).__name__ if ok else f"got {type(exc).__name__}, expected {exc_name}"
                print(json.dumps({"pass": ok, "reason": reason}))
        else:
            result = normalize(fn(**inputs))
            expected = normalize(json.loads(expected_json))
            ok = result == expected
            reason = "match" if ok else f"got {result!r}, expected {expected!r}"
            print(json.dumps({"pass": ok, "reason": reason}))
    except Exception as exc:
        print(json.dumps({"pass": False, "reason": f"execution error: {type(exc).__name__}: {exc}"}))
    '''
)


_HTTP_RUNNER_SCRIPT = textwrap.dedent(
    '''
    import json
    import os
    import sys
    from pathlib import Path

    out_dir = Path(sys.argv[1])   # dir containing the assembled app/ package
    route = sys.argv[2]
    inputs_json = sys.argv[3]
    expected_json = sys.argv[4]
    oracle = sys.argv[5]

    # cwd = the package dir so the app's sqlite:///./app.db is private to this sample.
    os.chdir(out_dir)
    sys.path.insert(0, str(out_dir))

    def normalize(value):
        if isinstance(value, dict):
            return {str(k): normalize(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [normalize(v) for v in value]
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return str(value)

    try:
        from app import create_app
        from fastapi.testclient import TestClient
        client = TestClient(create_app())
        inputs = json.loads(inputs_json)
        resp = client.post(route, json=inputs)
    except Exception as exc:
        print(json.dumps({"pass": False, "reason": f"app boot/request error: {type(exc).__name__}: {exc}"}))
        raise SystemExit(0)

    if oracle == "raises":
        # An HTTP error status is the web equivalent of a raised precondition failure.
        ok = resp.status_code >= 400
        print(json.dumps({"pass": ok, "reason": f"HTTP {resp.status_code}"}))
    elif resp.status_code != 200:
        print(json.dumps({"pass": False, "reason": f"HTTP {resp.status_code}: {resp.text[:160]}"}))
    else:
        try:
            body = normalize(resp.json())
        except Exception:
            print(json.dumps({"pass": False, "reason": f"non-JSON response: {resp.text[:160]}"}))
            raise SystemExit(0)
        expected = normalize(json.loads(expected_json))
        ok = body == expected
        reason = "match" if ok else f"got {body!r}, expected {expected!r}"
        print(json.dumps({"pass": ok, "reason": reason}))
    '''
)


def route_from_file_path(file_path: str) -> str:
    """The HTTP route the packager registers for a generated module.

    build_runnable_package() mounts each router under prefix ``/{layer}/{module_stem}`` and
    the Code Agent decorates with ``@router.post("")``, so the full route is deterministic:
    ``controllers/manage_menu_items.py`` -> ``/controllers/manage_menu_items``.
    """
    p = file_path[:-3] if file_path.endswith(".py") else file_path
    return "/" + p.strip("/")


def run_case_http(out_dir: Path, file_path: str, case: dict, timeout: float = 30.0) -> tuple[bool, str]:
    """Run one structured test case against the assembled FastAPI app via TestClient.

    Posts the case's canonical inputs to the module's route and checks the JSON response
    (oracle ``eq``) or that the call returns a 4xx error status (oracle ``raises``).
    """
    route = route_from_file_path(file_path)
    inputs_json = case.get("inputs_json") or "{}"
    expected_json = case.get("expected_json") or "null"
    oracle = case.get("oracle") or "eq"

    try:
        json.loads(inputs_json)
        json.loads(expected_json)
    except json.JSONDecodeError as exc:
        return False, f"invalid test JSON: {exc}"

    proc = subprocess.run(
        [sys.executable, "-c", _HTTP_RUNNER_SCRIPT, str(out_dir), route, inputs_json, expected_json, oracle],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        err = (proc.stderr or proc.stdout or "subprocess failed").strip()
        return False, err[:300]

    line = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    try:
        payload = json.loads(line)
    except json.JSONDecodeError:
        return False, (proc.stdout or proc.stderr or "no result")[:300]
    return bool(payload.get("pass")), str(payload.get("reason", ""))


def func_name_from_signature(signature: str) -> str | None:
    match = re.search(r"def\s+([A-Za-z_]\w*)", signature or "")
    return match.group(1) if match else None


def run_case(
    code_dir: Path,
    file_path: str,
    signature: str,
    case: dict,
    timeout: float = 10.0,
) -> tuple[bool, str]:
    """Run one structured test case. Returns (passed, reason)."""
    func_name = func_name_from_signature(signature)
    if not func_name:
        return False, "no function name in signature"

    inputs_json = case.get("inputs_json") or "{}"
    expected_json = case.get("expected_json") or "null"
    oracle = case.get("oracle") or "eq"

    try:
        json.loads(inputs_json)
        json.loads(expected_json)
    except json.JSONDecodeError as exc:
        return False, f"invalid test JSON: {exc}"

    proc = subprocess.run(
        [sys.executable, "-c", _RUNNER_SCRIPT, str(code_dir), file_path, func_name, inputs_json, expected_json, oracle],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        err = (proc.stderr or proc.stdout or "subprocess failed").strip()
        return False, err[:300]

    line = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    try:
        payload = json.loads(line)
    except json.JSONDecodeError:
        return False, (proc.stdout or proc.stderr or "no result")[:300]

    return bool(payload.get("pass")), str(payload.get("reason", ""))


def run_pytest_module(code_dir: Path, test_file: Path, timeout: float = 60.0) -> tuple[bool, str]:
    """Optional: run a pytest module with PYTHONPATH=code_dir."""
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_file), "-q", "--tb=line"],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=test_file.parent,
        env={**__import__("os").environ, "PYTHONPATH": str(code_dir)},
    )
    ok = proc.returncode == 0
    summary = (proc.stdout or proc.stderr or "").strip().splitlines()
    reason = summary[-1] if summary else ("passed" if ok else "pytest failed")
    return ok, reason[:300]
