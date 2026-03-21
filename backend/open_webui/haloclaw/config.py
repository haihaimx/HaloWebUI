import os

from open_webui.config import PersistentConfig

ENABLE_HALOCLAW = PersistentConfig(
    "ENABLE_HALOCLAW",
    "haloclaw.enable",
    os.environ.get("ENABLE_HALOCLAW", "False").lower() == "true",
)

HALOCLAW_DEFAULT_MODEL = PersistentConfig(
    "HALOCLAW_DEFAULT_MODEL",
    "haloclaw.default_model",
    os.environ.get("HALOCLAW_DEFAULT_MODEL", ""),
)

HALOCLAW_MAX_HISTORY = PersistentConfig(
    "HALOCLAW_MAX_HISTORY",
    "haloclaw.max_history",
    int(os.environ.get("HALOCLAW_MAX_HISTORY", "20")),
)

HALOCLAW_RATE_LIMIT = PersistentConfig(
    "HALOCLAW_RATE_LIMIT",
    "haloclaw.rate_limit",
    int(os.environ.get("HALOCLAW_RATE_LIMIT", "10")),
)
