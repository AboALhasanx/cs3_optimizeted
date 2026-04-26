# config.py
"""
Runtime configuration.

All values are read from environment variables (via .env or system env).
No hardcoded secrets.  The bot will raise RuntimeError on startup if
any required variable is missing.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def required_str(name):
    """Return the env var *name*, or raise RuntimeError if missing/empty."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            f"Set it in a .env file or as a system environment variable."
        )
    return value


def required_int(name):
    """Return the env var *name* as int, or raise RuntimeError."""
    raw = required_str(name)
    try:
        return int(raw)
    except ValueError:
        raise RuntimeError(
            f"Environment variable {name} must be an integer, "
            f"got {raw!r}."
        )


# Telegram bot token
BOT_TOKEN = required_str("BOT_TOKEN")

# Admin user ID
ADMIN_ID = required_int("ADMIN_ID")

# Channel IDs
cs_stg3 = required_int("CS_STG3")
cs_stg3_onefile = required_int("CS_STG3_ONEFILE")
cs_stg3_deleted = required_int("CS_STG3_DELETED")
cs_apps = required_int("CS_APPS")
LOG_CHANNEL_ID = required_int("LOG_CHANNEL_ID")

# Optional Telegram proxy URL (e.g. socks5h://127.0.0.1:9050 for Tor).
# Leave empty for a direct connection.
TELEGRAM_PROXY_URL = os.getenv("TELEGRAM_PROXY_URL", "").strip()
