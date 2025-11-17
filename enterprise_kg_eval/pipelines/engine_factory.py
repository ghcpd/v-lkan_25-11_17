from typing import Any
from ..engines import RegexEngine, LLMEngine, MLEngine


def get_engine(name: str, **kwargs) -> Any:
    name = name.lower()
    if name == "regex":
        return RegexEngine()
    if name == "llm":
        return LLMEngine(**kwargs)
    if name == "ml":
        return MLEngine()
    raise ValueError(f"Unknown engine: {name}")
