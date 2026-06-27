"""
SRS Reader for the Agentic Cleanroom Specification Generator Agent.

Responsibilities (all deterministic — no LLM involved):
  - Recursively parse an SRS XML at any nesting depth.
  - Assign every node a stable ID: the real `id` attribute if present,
    otherwise a position-based fallback.
  - Tag each node as "section" (grouping header) or "requirement".
  - Extract functional requirements ONLY from:
      * "Functional Requirements" sections (legacy req_document, e.g. video search),
      * ``SystemRequirements`` / ``<Feature>`` blocks (e.g. DineOut, Gemini),
      * PEPPOL/VCD ``req_document`` subsections with MUST/SHOULD/SHALL itemize bullets.

`<itemize>` handling is section-aware: everywhere else an itemize is an OVERVIEW list
and is skipped (so it never produces phantom requirements), but inside a
"Functional Requirements" section the itemize items ARE the requirements.

The LLM is intentionally kept OUT of IDs, structure, and grouping so that
those can never drift or hallucinate. The LLM's job downstream is only
interpretation (e.g. inferring inputs/outputs for feature-style SRS).
"""

import re
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


def _extract_itemize_items(tb) -> list[str]:
    """Return the text of every <item> inside any <itemize> under a <text_body>.

    Used ONLY for "Functional Requirements" sections, where each item (e.g.
    "REQ-1: ...") is a real requirement. Elsewhere itemize is skipped as overview.
    """
    items: list[str] = []
    for el in tb.iter():
        if _strip_ns(el.tag) == "item":
            text = _clean("".join(el.itertext()))
            if text:
                items.append(text)
    return items


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
    items: list[str] = []
    children = []
    child_index = 0

    for child in node:
        ctag = _strip_ns(child.tag)
        if ctag == "title":
            title = _clean("".join(child.itertext()))
        elif ctag == "text_body":
            body = _extract_text_body(child)
            items = _extract_itemize_items(child)
        elif ctag == "p":
            child_index += 1
            parsed = _parse_node(child, f"{node_id}.{child_index}")
            if parsed:
                children.append(parsed)

    return {"id": node_id, "title": title, "body": body, "items": items, "children": children}


# --------------------------------------------------------------------------
# FR-only, section-aware feature building
# --------------------------------------------------------------------------
FR_SECTION_TITLE = "functional requirements"  # the ONLY section title we extract from

# A leading "REQ-<n>:" label inside an <item>, e.g. "REQ-1: Torrent search will ...".
_REQ_LABEL = re.compile(r"^\s*REQ[-_\s]?(\d+)\s*[:.)\-]?\s*(.*)$", re.IGNORECASE | re.DOTALL)

# Normative RFC 2119 language in PEPPOL-style ``req_document`` itemize bullets.
_NORMATIVE = re.compile(
    r"\b(MUST NOT|SHALL NOT|SHOULD NOT|MUST|SHALL|SHOULD)\b",
    re.IGNORECASE,
)


def _is_fr_section(node: dict) -> bool:
    """True iff this node's title is exactly 'Functional Requirements' (case-insensitive)."""
    return _clean(node.get("title", "")).lower() == FR_SECTION_TITLE


def _parse_req_item(item_text: str) -> tuple[str | None, str]:
    """Split an itemize entry into ('REQ-<n>', body); label is None if no REQ prefix."""
    m = _REQ_LABEL.match(item_text)
    if m:
        return f"REQ-{int(m.group(1))}", _clean(m.group(2))
    return None, _clean(item_text)


def _feature_description(parent: dict) -> str:
    """A feature's blurb: its own text, else its 'Description and Priority' child's text."""
    if parent.get("body"):
        return parent["body"]
    for child in parent.get("children", []):
        if "description" in _clean(child.get("title", "")).lower():
            return child.get("body", "")
    return ""


def build_fr_features(tree: list[dict]) -> list[dict]:
    """Build features from FUNCTIONAL-REQUIREMENT sections only.

    Walk the parsed tree; whenever a node's title is "Functional Requirements", its
    PARENT is the feature and the section's <itemize> items (REQ-N) are that feature's
    requirements. IDs are derived purely from structure: '<feature_id>.REQ-<n>'.
    Narrative and non-functional sections are never visited for extraction.
    """
    features: dict[str, dict] = {}
    order: list[str] = []

    def add_feature(parent: dict, fr_node: dict) -> None:
        feature_id = parent["id"]
        if feature_id not in features:
            features[feature_id] = {
                "id": feature_id,
                "name": parent.get("title") or feature_id,
                "description": _feature_description(parent),
                "functional_requirements": [],
            }
            order.append(feature_id)
        reqs = features[feature_id]["functional_requirements"]

        items = fr_node.get("items", [])
        if items:
            for idx, item in enumerate(items, start=1):
                label, text = _parse_req_item(item)
                req_id = f"{feature_id}.{label or f'REQ-{idx}'}"
                reqs.append({"id": req_id, "text": text})
        else:
            # Fallback for SRS variants that nest FR sub-<p> nodes instead of itemize.
            for child in fr_node.get("children", []):
                text = child.get("body") or child.get("title")
                if text:
                    reqs.append({"id": child["id"], "text": text})
            # Gemini-style: prose requirement(s) directly in the FR section body (no itemize).
            body = _clean(fr_node.get("body", ""))
            if body and not any(r.get("text") == body for r in reqs):
                reqs.append({"id": f"{feature_id}.REQ-{len(reqs) + 1}", "text": body})

    def walk(node: dict) -> None:
        for child in node.get("children", []):
            if _is_fr_section(child):
                add_feature(node, child)
            walk(child)

    for root in tree:
        walk(root)

    return [features[k] for k in order]


def _is_nfr_section_title(title: str) -> bool:
    """Skip sections that are explicitly non-functional requirement lists."""
    t = _clean(title).lower()
    return "non-functional" in t or "non functional" in t


def _normative_items(node: dict) -> list[str]:
    """Itemize entries that contain RFC 2119 normative keywords."""
    return [item for item in node.get("items", []) if _NORMATIVE.search(item)]


def build_peppol_normative_features(tree: list[dict]) -> list[dict]:
    """Build features from PEPPOL / VCD ``req_document`` SRS variants.

    Each ``<p>`` subsection whose itemize list contains MUST/SHOULD/SHALL bullets
    becomes one feature; each normative bullet becomes ``<feature_id>.REQ-<n>``.
    Used when the document has no explicit "Functional Requirements" sections.
    """
    features: dict[str, dict] = {}
    order: list[str] = []

    def add_feature(node: dict, items: list[str]) -> None:
        feature_id = node["id"]
        if feature_id not in features:
            features[feature_id] = {
                "id": feature_id,
                "name": node.get("title") or feature_id,
                "description": node.get("body", ""),
                "functional_requirements": [],
            }
            order.append(feature_id)
        reqs = features[feature_id]["functional_requirements"]
        for idx, item in enumerate(items, start=len(reqs) + 1):
            label, text = _parse_req_item(item)
            req_id = f"{feature_id}.{label or f'REQ-{idx}'}"
            reqs.append({"id": req_id, "text": text})

    def walk(node: dict) -> None:
        if _is_nfr_section_title(node.get("title", "")):
            for child in node.get("children", []):
                walk(child)
            return
        items = _normative_items(node)
        if items:
            add_feature(node, items)
        for child in node.get("children", []):
            walk(child)

    for root in tree:
        walk(root)

    return [features[k] for k in order if features[k]["functional_requirements"]]


def build_userclass_features(root) -> list[dict]:
    """SRS variant: ``<SRS><FunctionalRequirements>`` grouping ``<UserClass>`` blocks of
    ``<Requirement>`` (e.g. kinmail).

    Example::

        <FunctionalRequirements>
          <UserClass id="1" name="Non Registered Users">
            <Requirement id="4.1.1"><Title>..</Title><Desc>..</Desc></Requirement>

    Each ``<UserClass>`` becomes a feature; each ``<Requirement>`` is one FR — id from the
    ``id`` attribute, text from ``<Desc>`` (falling back to all descendant text). If there is
    no ``<UserClass>`` grouping, the whole ``<FunctionalRequirements>`` block is one feature.
    """
    fr = root.find(".//FunctionalRequirements")
    if fr is None:
        return []

    features: list[dict] = []
    classes = [c for c in fr if _strip_ns(c.tag) == "UserClass"]
    groups = classes or [fr]
    for grp in groups:
        feature_id = grp.get("id") or str(len(features) + 1)
        name = grp.get("name") or grp.get("id") or feature_id
        reqs: list[dict] = []
        for req in grp.iter():
            if _strip_ns(req.tag) != "Requirement":
                continue
            desc_el = next((e for e in req if _strip_ns(e.tag) == "Desc"), None)
            src = desc_el if desc_el is not None else req
            text = _clean("".join(src.itertext()))
            if text:
                reqs.append({"id": req.get("id") or f"{feature_id}.REQ-{len(reqs) + 1}", "text": text})
        if reqs:
            features.append({
                "id": feature_id,
                "name": name,
                "description": "",
                "functional_requirements": reqs,
            })
    return features


def _is_modules_fr_section(title: str) -> bool:
    """A section whose title CONTAINS 'functional requirements' but is not the non-functional
    list (e.g. 'Description of the Modules and Functional Requirements')."""
    t = _clean(title).lower()
    return "functional requirements" in t and "non-functional" not in t and "non functional" not in t


def build_module_section_features(tree: list[dict]) -> list[dict]:
    """Last-resort ``req_document`` fallback (e.g. cctns).

    Used only when no exact "Functional Requirements" section exists. Finds a section whose
    title CONTAINS "functional requirements" and treats each of its child ``<p>`` nodes as a
    module/feature: the module's prose body becomes ``<id>.REQ-1`` and any nested ``<p>``
    bodies / itemize items become further requirements.
    """
    features: list[dict] = []

    def module_to_feature(mod: dict) -> dict | None:
        reqs: list[dict] = []
        for idx, item in enumerate(mod.get("items", []), start=1):
            label, text = _parse_req_item(item)
            if text:
                reqs.append({"id": f"{mod['id']}.{label or f'REQ-{idx}'}", "text": text})
        body = _clean(mod.get("body", ""))
        if body and not any(r["text"] == body for r in reqs):
            reqs.insert(0, {"id": f"{mod['id']}.REQ-1", "text": body})
        for child in mod.get("children", []):
            ctext = _clean(child.get("body") or child.get("title") or "")
            if ctext:
                reqs.append({"id": child["id"], "text": ctext})
        if not reqs:
            return None
        return {
            "id": mod["id"],
            "name": mod.get("title") or mod["id"],
            "description": body,
            "functional_requirements": reqs,
        }

    seen: set[str] = set()

    def walk(node: dict) -> None:
        # Check the node itself: a modules section can be a top-level root or nested.
        if _is_modules_fr_section(node.get("title", "")):
            for mod in node.get("children", []):
                feat = module_to_feature(mod)
                if feat and feat["id"] not in seen:
                    seen.add(feat["id"])
                    features.append(feat)
        for child in node.get("children", []):
            walk(child)

    for root in tree:
        walk(root)
    return features


def build_system_requirements_features(root) -> list[dict]:
    """Parse SRS variants that declare features directly under ``SystemRequirements``.

    Example (DineOut): ``<Feature id="4.1" name="Place Order"><Description>...</Description></Feature>``.
    Each feature's ``Description`` becomes a single functional requirement (``<id>.REQ-1``).
    Non-functional sections elsewhere in the document are ignored.
    """
    sr = root.find(".//SystemRequirements")
    if sr is None:
        return []

    features: list[dict] = []
    for feat in sr:
        if _strip_ns(feat.tag) != "Feature":
            continue
        feature_id = feat.get("id") or str(len(features) + 1)
        name = feat.get("name") or feature_id
        desc_el = feat.find("Description")
        if desc_el is not None:
            description = _clean("".join(desc_el.itertext()))
        else:
            # Gemini-style: requirement text directly inside <Feature> with no <Description>.
            description = _clean(feat.text or "")

        frs: list[dict] = []
        if description:
            frs.append({"id": f"{feature_id}.REQ-1", "text": description})
        # Nested itemize under the feature (if present) adds further REQ-N entries.
        for idx, item in enumerate(_extract_itemize_items(feat), start=2 if description else 1):
            label, text = _parse_req_item(item)
            frs.append({"id": f"{feature_id}.{label or f'REQ-{idx}'}", "text": text})

        if frs:
            features.append({
                "id": feature_id,
                "name": name,
                "description": description,
                "functional_requirements": frs,
            })
    return features


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

    def read_features(self, path: Path) -> list[dict]:
        """Functional requirements grouped into features (FR-only, section-aware).

        Supports three deterministic SRS shapes:
          1. Legacy ``req_document`` with nested ``<p>`` nodes and a "Functional Requirements"
             section per feature (itemize items become REQ-N).
          2. ``SystemRequirements`` / ``<Feature>`` lists (e.g. DineOut) where each feature's
             ``Description`` (or inline body text) becomes ``<feature_id>.REQ-1``.
          3. PEPPOL / VCD ``req_document`` with normative MUST/SHOULD/SHALL itemize bullets
             under requirement subsections (each subsection becomes a feature).
        """
        if not path.exists():
            raise FileNotFoundError(f"SRS file not found: {path}")
        doc = etree.parse(str(path))
        root = doc.getroot()
        tree = self.read_tree(path)

        features = build_fr_features(tree)
        if features:
            return features
        features = build_system_requirements_features(root)
        if features:
            return features
        # <SRS><FunctionalRequirements><UserClass><Requirement> (e.g. kinmail).
        features = build_userclass_features(root)
        if features:
            return features
        features = build_peppol_normative_features(tree)
        if features:
            return features
        # Last resort: a "… Modules and Functional Requirements" section of prose modules
        # (e.g. cctns). Only reached when nothing above matched, so working SRS are untouched.
        return build_module_section_features(tree)


if __name__ == "__main__":
    import sys

    reader = SRSReader()
    path = Path(sys.argv[1])
    feats = reader.read_features(path)
    total = sum(len(f["functional_requirements"]) for f in feats)
    print(f"{path.name}: {len(feats)} features, {total} requirements\n")
    for f in feats:
        print(f"[{f['id']}] {f['name']} -> {len(f['functional_requirements'])} reqs")