"""Configuration management (env vars + .env file, stdlib only)."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _load_dotenv(path: Path | None = None) -> None:
    """Minimal .env loader: KEY=VALUE lines, ignores comments. No overrides."""
    candidates = [path] if path else [Path.cwd() / ".env", Path(__file__).resolve().parents[2] / ".env"]
    for cand in candidates:
        if cand is None or not cand.exists():
            continue
        for line in cand.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip().strip("'\"")
            if key and key not in os.environ:
                os.environ[key] = val


_load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Runtime settings. All fields overridable via environment."""

    llm_provider: str = field(default_factory=lambda: os.environ.get("PHYSICS_AGENT_LLM_PROVIDER", "echo"))
    llm_model: str = field(default_factory=lambda: os.environ.get("PHYSICS_AGENT_LLM_MODEL", "echo-1"))
    openai_base_url: str = field(default_factory=lambda: os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    openai_api_key: str = field(default_factory=lambda: os.environ.get("OPENAI_API_KEY", ""))
    level: int = field(default_factory=lambda: int(os.environ.get("PHYSICS_AGENT_LEVEL", "2")))
    mode: str = field(default_factory=lambda: os.environ.get("PHYSICS_AGENT_MODE", "direct"))
    data_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parents[2] / "data")

    def __post_init__(self) -> None:
        if self.level not in (1, 2, 3, 4):
            raise ValueError("level must be 1..4")


_settings: Settings | None = None


def get_settings() -> Settings:
    """Return the cached process-wide Settings."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
