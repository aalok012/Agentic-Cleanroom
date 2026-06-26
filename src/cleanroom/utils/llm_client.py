import json
import os
import re

from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

from src.cleanroom.llms.callbacks.metric import GLOBAL_HANDLER

load_dotenv(override=True)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Short names used across the pipeline; resolve_model() maps them for OpenRouter when configured.
DEFAULT_MODEL = "gpt-4o-mini"
DAFNY_MODEL = "gpt-4.1"


def _extract_json(text: str | None) -> dict | None:
    """Best-effort pull of a JSON object out of free text — strips ```json fences and surrounding
    prose, then loads the outermost {...}. Returns None if nothing parseable is found."""
    if not text:
        return None
    t = text.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", t, re.S)
    if fence:
        t = fence.group(1).strip()
    start, end = t.find("{"), t.rfind("}")
    if start != -1 and end > start:
        t = t[start : end + 1]
    try:
        obj = json.loads(t)
        return obj if isinstance(obj, dict) else None
    except Exception:
        return None


def _coerce_structured(d: dict, schema):
    """Turn the `include_raw=True` envelope ({raw, parsed, parsing_error}) back into the parsed
    object — but if the tool call was absent or failed to validate, recover the data from the
    message's tool-call args or its text content (some models, esp. 'thinking' ones, answer in
    prose/fenced JSON instead of emitting a clean tool call). Returns None only if nothing is
    recoverable, so callers that tolerate emptiness (e.g. dependency edges) still see None."""
    parsed = d.get("parsed") if isinstance(d, dict) else None
    if parsed is not None:
        return parsed                                  # normal path — no behavior change
    if not hasattr(schema, "model_validate"):
        return parsed
    raw = d.get("raw") if isinstance(d, dict) else None
    # 1) a tool call was made but its args failed strict validation — try a lenient re-validate
    for tc in (getattr(raw, "tool_calls", None) or []):
        args = tc.get("args") if isinstance(tc, dict) else None
        if isinstance(args, dict):
            try:
                return schema.model_validate(args)
            except Exception:
                pass
    # 2) no usable tool call — recover JSON from the message content
    content = getattr(raw, "content", None)
    text = content if isinstance(content, str) else (
        "".join(b.get("text", "") for b in content if isinstance(b, dict)) if isinstance(content, list) else None
    )
    obj = _extract_json(text)
    if obj is not None:
        try:
            return schema.model_validate(obj)
        except Exception:
            pass
    return None


class _ChatOpenAI(ChatOpenAI):
    """ChatOpenAI hardened for the mixed-model pipeline. Two changes to `with_structured_output`:

    1. Default method is `function_calling`, not langchain's `json_schema`. OpenAI/Anthropic honor
       strict json_schema, but open-weight models on OpenRouter wrap the JSON in a ```json fence,
       which the strict parser rejects. Tool-calling args are provider-normalized and work for all.
    2. We request `include_raw=True` under the hood and post-process: if the model emits no clean
       tool call (common for 'thinking' models that answer in prose), we recover the structured
       data from its tool-call args or message content instead of returning None. The agent still
       receives the parsed pydantic object — the recovery is invisible to callers.

    A caller passing `include_raw=True` itself gets the raw envelope untouched; an explicit
    `method=` overrides the default.
    """

    def with_structured_output(self, schema=None, *, method="function_calling",
                               include_raw=False, **kwargs):
        base = super().with_structured_output(
            schema, method=method, include_raw=True, **kwargs)
        if include_raw:
            return base                                # caller asked for the raw envelope
        return base | RunnableLambda(lambda d, _s=schema: _coerce_structured(d, _s))


def _using_openrouter() -> bool:
    if os.getenv("OPENROUTER_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        return True
    base = (os.getenv("OPENAI_BASE_URL") or "").lower()
    return "openrouter.ai" in base


def llm_api_key() -> str | None:
    """API key for ChatOpenAI — OpenRouter or direct OpenAI."""
    return os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")


def llm_api_key_configured() -> bool:
    return bool(llm_api_key())


def resolve_model(name: str) -> str:
    """Map a short model name to an OpenRouter slug when routing through OpenRouter."""
    if "/" in name:
        return name
    prefix = os.getenv("LLM_MODEL_PREFIX", "")
    if not prefix and _using_openrouter():
        prefix = "openai/"
    return f"{prefix}{name}" if prefix else name


def get_llm(model: str = DEFAULT_MODEL, temperature: float = 0.0) -> ChatOpenAI:
    # temperature defaults to 0 (deterministic) for the generation/judging stages;
    # the certification stage raises it to draw diverse samples for pass@k.
    # GLOBAL_HANDLER counts tokens/latency for every call (counts only, no content).
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    # If only OPENROUTER_API_KEY is set, automatically route to OpenRouter
    # without requiring OPENAI_BASE_URL to be set.
    if openrouter_key and not openai_key:
        base_url = OPENROUTER_BASE_URL
        api_key = openrouter_key
    else:
        base_url = os.getenv("OPENAI_BASE_URL")
        api_key = openai_key or openrouter_key

    default_headers: dict[str, str] = {}
    if referer := os.getenv("OPENROUTER_HTTP_REFERER"):
        default_headers["HTTP-Referer"] = referer
    if title := os.getenv("OPENROUTER_X_TITLE"):
        default_headers["X-Title"] = title

    kwargs: dict = {
        "model": resolve_model(model),
        "temperature": temperature,
        "api_key": api_key,
        "callbacks": [GLOBAL_HANDLER],
    }
    if base_url:
        kwargs["base_url"] = base_url
    if default_headers:
        kwargs["default_headers"] = default_headers

    # OpenRouter provider routing. By default we let OpenRouter pick the provider: with
    # function-calling structured output (see _ChatOpenAI), the default routing already returns
    # proper tool calls for open models. Opt in to strict capability matching with
    # OPENROUTER_REQUIRE_PARAMETERS=1 — but note it can over-constrain routing to a 404
    # ("No endpoints found that can handle the requested parameters") when tools are in play.
    on_openrouter = (openrouter_key and not openai_key) or "openrouter.ai" in (base_url or "").lower()
    if on_openrouter and os.getenv("OPENROUTER_REQUIRE_PARAMETERS", "").lower() in ("1", "true", "yes"):
        kwargs["extra_body"] = {"provider": {"require_parameters": True}}

    # _ChatOpenAI defaults structured output to function/tool calling (see class docstring) so
    # open models on OpenRouter work; for OpenAI/Anthropic it behaves the same as plain ChatOpenAI.
    return _ChatOpenAI(**kwargs)
