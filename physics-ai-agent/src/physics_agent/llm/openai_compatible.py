"""OpenAI-compatible client (stdlib urllib): OpenAI, vLLM, Ollama, LM Studio..."""
from __future__ import annotations

import json
import urllib.request

from physics_agent.config import get_settings
from physics_agent.llm.base import LLMProvider, Message
from physics_agent.llm.echo import EchoProvider


class OpenAICompatibleProvider(LLMProvider):
    name = "openai_compatible"

    SYSTEM_GUARD = (
        "You are the narration layer of a physics reasoning engine. "
        "Deterministic tools already computed every number you see; "
        "NEVER recompute, adjust, or invent numeric values, and never invent "
        "equations, references, or material data. If a value is missing, say so."
    )

    def __init__(self, base_url: str | None = None, api_key: str | None = None,
                 model: str | None = None, timeout: float = 60.0):
        s = get_settings()
        self.base_url = (base_url or s.openai_base_url).rstrip("/")
        self.api_key = api_key if api_key is not None else s.openai_api_key
        self.model = model or s.llm_model
        self.timeout = timeout

    def complete(self, messages: list[Message], max_tokens: int = 1024) -> str:
        payload = json.dumps({
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "max_tokens": max_tokens, "temperature": 0.2,
        }).encode()
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions", data=payload,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {self.api_key}"},
            method="POST")
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            data = json.loads(r.read().decode())
        return data["choices"][0]["message"]["content"]


def provider_from_env() -> LLMProvider:
    s = get_settings()
    if s.llm_provider == "openai_compatible" and s.openai_api_key:
        return OpenAICompatibleProvider()
    return EchoProvider()
