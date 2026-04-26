# config.py
"""
Runtime configuration.

Reads values from environment variables first (via .env file or system env).
Falls back to the hardcoded defaults below for local development.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram bot token
_BOT_TOKEN_DEFAULT = "7383156007:AAFqgYzWzUoHMnq0shgnzooE38ssKeXgj1k"
BOT_TOKEN = os.getenv("BOT_TOKEN", _BOT_TOKEN_DEFAULT)

# Admin user ID
_ADMIN_ID_DEFAULT = 5664798395
ADMIN_ID = int(os.getenv("ADMIN_ID", str(_ADMIN_ID_DEFAULT)))

# Channel IDs
_CS_STG3_DEFAULT = -1001905412532
cs_stg3 = int(os.getenv("CS_STG3", str(_CS_STG3_DEFAULT)))

_CS_STG3_ONEFILE_DEFAULT = -1001731774536
cs_stg3_onefile = int(os.getenv("CS_STG3_ONEFILE", str(_CS_STG3_ONEFILE_DEFAULT)))

_CS_STG3_DELETED_DEFAULT = -1001986350997
cs_stg3_deleted = int(os.getenv("CS_STG3_DELETED", str(_CS_STG3_DELETED_DEFAULT)))

_CS_APPS_DEFAULT = -1001802771388
cs_apps = int(os.getenv("CS_APPS", str(_CS_APPS_DEFAULT)))

_LOG_CHANNEL_ID_DEFAULT = -1003040612379
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", str(_LOG_CHANNEL_ID_DEFAULT)))

