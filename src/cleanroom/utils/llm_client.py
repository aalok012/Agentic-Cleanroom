import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from src.cleanroom.llms.callbacks.metric import GLOBAL_HANDLER

load_dotenv(override=True)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Short names used across the pipeline; resolve_model() maps them for OpenRouter when configured.
DEFAULT_MODEL = "gpt-4o-mini"
DAFNY_MODEL = "gpt-4.1"


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
    return ChatOpenAI(**kwargs)
