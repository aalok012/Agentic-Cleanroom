from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from src.cleanroom.llms.callbacks.metric import GLOBAL_HANDLER

load_dotenv()


def get_llm(model: str = "gpt-4o-mini", temperature: float = 0.0) -> ChatOpenAI:
    # temperature defaults to 0 (deterministic) for the generation/judging stages;
    # the certification stage raises it to draw diverse samples for pass@k.
    # GLOBAL_HANDLER counts tokens/latency for every call (counts only, no content).
    return ChatOpenAI(model=model, temperature=temperature, callbacks=[GLOBAL_HANDLER])
