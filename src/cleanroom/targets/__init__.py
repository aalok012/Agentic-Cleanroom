"""Language targets — per-language knobs (codegen/test templates, packaging, oracle).

`get_target(language)` returns the `LanguageTarget` the agents dispatch through, so adding a
language is a new subclass + its prompts, not edits scattered across the agents.
"""

from src.cleanroom.targets.base import LanguageTarget
from src.cleanroom.targets.java import JavaTarget

_TARGETS: dict[str, LanguageTarget] = {"python": LanguageTarget(), "java": JavaTarget()}


def get_target(language: str) -> LanguageTarget:
    return _TARGETS.get(language, _TARGETS["python"])


__all__ = ["LanguageTarget", "JavaTarget", "get_target"]
