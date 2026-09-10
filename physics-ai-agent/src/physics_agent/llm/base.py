"""LLM interface. Physics engine stays independent of any provider."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Message:
    role: str  # system | user | assistant
    content: str


class LLMProvider(ABC):
    """Narrative reasoning + explanation. Must NOT do critical numerics."""

    name: str = "base"

    @abstractmethod
    def complete(self, messages: list[Message], max_tokens: int = 1024) -> str:
        ...

    def explain(self, system: str, user: str) -> str:
        return self.complete([Message("system", system), Message("user", user)])
