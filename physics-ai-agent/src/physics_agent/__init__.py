"""Physics AI Agent — interactive physics reasoning engine.

LLM reasons about the problem; deterministic tools compute the answer.
"""

__version__ = "0.2.0"

from physics_agent.config import Settings, get_settings

__all__ = ["__version__", "Settings", "get_settings"]
