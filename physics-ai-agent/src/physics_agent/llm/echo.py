"""Deterministic offline provider: template-based narration, zero network.

Used by default and in tests. Numeric answers always come from the solver
layer; this provider only wraps them in prose when asked.
"""
from __future__ import annotations

from physics_agent.llm.base import LLMProvider, Message


class EchoProvider(LLMProvider):
    """Deterministic offline provider: template narration, zero network."""
    name = "echo"

    def complete(self, messages: list[Message], max_tokens: int = 1024) -> str:
        """Narrate the request from a fixed template."""
        user = next((m.content for m in reversed(messages) if m.role == "user"), "")
        return (
            "[echo provider — offline narration]\n"
            f"You asked: {user[:400]}\n"
            "The deterministic physics pipeline (classifier → solvers → verification) "
            "produced the structured report below. Configure PHYSICS_AGENT_LLM_PROVIDER="
            "openai_compatible + OPENAI_API_KEY for free-form LLM narration."
        )
