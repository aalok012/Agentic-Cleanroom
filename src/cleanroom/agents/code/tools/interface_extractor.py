"""Extract the *interface* (signatures only) from generated Python source.

Deterministic, no LLM. When increment B depends on increment A, the Code Agent
hands B only A's public signatures — never A's full implementation and never the
whole IR. This keeps per-increment prompts small (token discipline) while still
letting B call correctly into A.
"""

import ast
import re


def _is_public(name: str) -> bool:
    return name == "__init__" or not name.startswith("_")


def _regex_signatures(content: str) -> str:
    """Fallback for non-Python or syntactically invalid content: grab def/class lines."""
    sigs = re.findall(r"^\s*(?:class|def)\s+[^\n]*?:", content, re.MULTILINE)
    return "\n".join(s.strip() for s in sigs)


def extract_interface(content: str) -> str:
    """Return public class/method/function signatures (no bodies) from Python source."""
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return _regex_signatures(content)

    lines: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            lines.append(f"class {node.name}:")
            methods = [
                f"    def {item.name}({ast.unparse(item.args)}): ..."
                for item in node.body
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and _is_public(item.name)
            ]
            lines.extend(methods or ["    ..."])
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and _is_public(node.name):
            lines.append(f"def {node.name}({ast.unparse(node.args)}): ...")
    return "\n".join(lines)
