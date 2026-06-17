"""
SRS Reader for the Agentic Cleanroom Specification Generator Agent.

Responsibilities (all deterministic — no LLM involved):
  - Recursively parse an SRS XML at any nesting depth.
  - Assign every node a stable ID: the real `id` attribute if present,
    otherwise a position-based fallback.
  - Tag each node as "section" (grouping header) or "requirement".
  - Group requirements under their feature by ID prefix.
  - Give every feature its own description so childless features
    (e.g. Security, Privacy) are never left empty.

The LLM is intentionally kept OUT of IDs, structure, and grouping so that
those can never drift or hallucinate. The LLM's job downstream is only
interpretation (e.g. inferring inputs/outputs for feature-style SRS).
"""

from pathlib import Path

from lxml import etree


# --------------------------------------------------------------------------
# low-level helpers
# --------------------------------------------------------------------------
def _strip_ns(tag: str) -> str:
    """Drop the namespace prefix from a tag name (lxml gives '{ns}tag')."""
    return tag.split("}")[-1] if "}" in tag else tag


def _clean(text: str | None) -> str:
    """Collapse all whitespace/newlines into single spaces."""
    if not text:
        return ""
    return " ".join(text.split())


def _extract_text_body(tb) -> str:
    """
    Extract the text of a <text_body>.
    Skips <itemize> overview lists, because those summarize the real sections
    and would otherwise create duplicate requirements.
    """
    parts = []
    if tb.text:
        parts.append(_clean(tb.text))
    for el in tb:
        if _strip_ns(el.tag) == "itemize":
            continue  # overview list — real sections carry these requirements
        text = _clean("".join(el.itertext()))
        if text:
            parts.append(text)
        if el.tail:
            parts.append(_clean(el.tail))
    return " ".join(p for p in parts if p)


# --------------------------------------------------------------------------
# parsing
# --------------------------------------------------------------------------
def _parse_node(node, fallback_id: str) -> dict | None:
    """Recursively parse a <p> node into {id, title, body, children}."""
    if _strip_ns(node.tag) != "p":
        return None

    # real id if present, else position-based fallback (handles SRS w/o ids)
    node_id = node.get("id") or fallback_id

    title = ""
    body = ""
    children = []
    child_index = 0

    for child in node:
        ctag = _strip_ns(child.tag)
        if ctag == "title":
            title = _clean("".join(child.itertext()))
        elif ctag == "text_body":
            body = _extract_text_body(child)
        elif ctag == "p":
            child_index += 1
            parsed = _parse_node(child, f"{node_id}.{child_index}")
            if parsed:
                children.append(parsed)

    return {"id": node_id, "title": title, "body": body, "children": children}


def _classify(node: dict) -> str:
    """
    Deterministic tag:
      section     = grouping header (has children, no requirement text of its own)
      requirement = carries an actual statement
    Errs toward 'requirement' (safe direction — better to over-include).
    """
    has_children = len(node["children"]) > 0
    has_text = bool(node["body"])
    if has_children and not has_text:
        return "section"
    return "requirement"


def _flatten(node: dict, out: list) -> None:
    out.append(
        {
            "id": node["id"],
            "type": _classify(node),
            "title": node["title"],
            "text": node["body"],
        }
    )
    for child in node["children"]:
        _flatten(child, out)


# --------------------------------------------------------------------------
# grouping
# --------------------------------------------------------------------------
def feature_key(node_id: str) -> str:
    """
    The feature an ID belongs to = its first two dot-segments.
    '2.2.6.9' -> '2.2'   '2.2.1.1a' -> '2.2'   '2.5' -> '2.5'
    """
    parts = node_id.split(".")
    if len(parts) <= 2:
        return node_id
    return ".".join(parts[:2])


def group_into_features(reqs: list[dict]) -> list[dict]:
    """
    Group requirements under their feature using ID prefixes.
    Each feature carries its own description (from its node's text), so
    childless features are never empty.
    """
    by_id = {r["id"]: r for r in reqs}

    features: dict[str, dict] = {}
    order: list[str] = []

    for r in reqs:
        if "." not in r["id"]:
            continue  # skip top-level document prose (intro / preamble)

        key = feature_key(r["id"])
        if key not in features:
            header = by_id.get(key, {})
            features[key] = {
                "feature_id": key,
                "name": header.get("title") or key,
                "description": header.get("text", ""),
                "functional_requirements": [],
            }
            order.append(key)

        if r["id"] == key:
            continue  # the feature header itself isn't its own sub-requirement
        if r["type"] == "requirement":
            features[key]["functional_requirements"].append(
                {"id": r["id"], "description": r["text"] or r["title"]}
            )

    return [features[k] for k in order]


# --------------------------------------------------------------------------
# public API
# --------------------------------------------------------------------------
class SRSReader:
    def read_tree(self, path: Path) -> list[dict]:
        """Full nested tree of the document."""
        if not path.exists():
            raise FileNotFoundError(f"SRS file not found: {path}")
        tree = etree.parse(str(path))
        root = tree.getroot()

        sections = []
        idx = 0
        for child in root:
            if _strip_ns(child.tag) == "p":
                idx += 1
                parsed = _parse_node(child, str(idx))
                if parsed:
                    sections.append(parsed)
        return sections

    def read_requirements(self, path: Path) -> list[dict]:
        """Flat, de-duplicated list of every node: {id, type, title, text}.
        IDs are 100% from the parser — the LLM never assigns them."""
        flat: list[dict] = []
        for s in self.read_tree(path):
            _flatten(s, flat)

        seen = set()
        deduped = []
        for r in flat:
            if r["id"] in seen:
                continue
            seen.add(r["id"])
            deduped.append(r)
        return deduped

    def read_features(self, path: Path) -> list[dict]:
        """Requirements grouped into features. This is the structural IR."""
        return group_into_features(self.read_requirements(path))

    def read(self, path: Path) -> str:
        """
        Human/LLM-facing text view. Every requirement on its own line with
        its ID bracketed at the front, so ID<->text binding is unambiguous.
        Use this only if you want the LLM to add interpretation on top.
        """
        lines = []
        for r in self.read_requirements(path):
            label = f"[{r['id']}]"
            tag = "" if r["type"] == "requirement" else " (section)"
            if r["title"] and r["text"]:
                lines.append(f"{label}{tag} {r['title']}: {r['text']}")
            elif r["title"]:
                lines.append(f"{label}{tag} {r['title']}")
            elif r["text"]:
                lines.append(f"{label}{tag} {r['text']}")
        return "\n".join(lines)


if __name__ == "__main__":
    import sys

    reader = SRSReader()
    path = Path(sys.argv[1])
    feats = reader.read_features(path)
    total = sum(len(f["functional_requirements"]) for f in feats)
    print(f"{path.name}: {len(feats)} features, {total} requirements\n")
    for f in feats:
        print(f"[{f['feature_id']}] {f['name']} -> {len(f['functional_requirements'])} reqs")