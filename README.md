# CS3 Telegram Bot — Project Architecture

A Telegram bot for third-year Computer Science students (University of Wasit),
built with [`pyTelegramBotAPI`](https://pytba.readthedocs.io/).

---

## Architecture Overview

```
cs3/
├── main.py                           ← Bot entry point
├── config.py                         ← Tokens & channel IDs
├── global_vars.py                    ← UI strings & emoji prefixes
├── term1_keyboard.py                 ← Term 1 keyboard definitions
├── term2_keyboard.py                 ← Term 2 keyboard definitions
├── data/
│   └── content_items.json            ← **RUNTIME** content catalog
├── services/
│   └── content_registry.py           ← Reads & validates the catalog
├── scripts/
│   ├── validate_content_items.py     ← Validates content_items.json
│   └── check_content_registry.py     ← Smoke-test for ContentRegistry
```

---

## 1. Runtime Content Lookup

**`main.py` uses `services/content_registry.py`** for all content-button
lookups and message-ID resolution.

```python
from services.content_registry import ContentRegistry

content_registry = ContentRegistry()

# Handler filter — checks the catalog for a matching button label
@bot.message_handler(func=lambda msg:
    content_registry.get_command_for_button(msg.text) is not None)
def handle_button(message):
    command = content_registry.get_command_for_button(message.text)
    get_file_command(message, command)
```

Inside `get_file_command()`, the channel ID is derived from the
`channel_key` field in the catalog, and `message_ids` is iterated to
forward each Telegram post.

---

## 2. Content Catalog (Single Source of Truth)

**`data/content_items.json`** is the sole runtime content catalog.

Each entry contains:

```json
{
    "id": 1,
    "button_label": "المادة في ملف واحد كاملة 📁🤖",
    "command_key": "ai_lab_in_old",
    "channel_key": "cs_stg3_deleted",
    "message_ids": [36],
    "active": true
}
```

| Field | Description |
|---|---|
| `id` | Unique sequential identifier |
| `button_label` | The text shown on the Telegram reply keyboard |
| `command_key` | Internal command name (used as lookup key) |
| `channel_key` | Symbolic channel identifier (mapped to real IDs in `config.py`) |
| `message_ids` | One or more Telegram message IDs to forward |
| `active` | Whether the button is currently available |

**Adding new content**: edit only `data/content_items.json`. Do **not**
edit the old JSON files listed below.

## 3. Validation

**`scripts/validate_content_items.py`** validates the catalog in
isolation:

- Counts total / active / inactive items
- Checks for duplicate `button_label` and `command_key`
- Verifies all active items have a `channel_key`, non-empty
  `message_ids`, and integer message IDs

Run it with:

```powershell
python scripts\validate_content_items.py
```

---

## 4. Smoke-Test for ContentRegistry

**`scripts/check_content_registry.py`** is a quick health-check that
instantiates `ContentRegistry`, loads the catalog, and runs the full
validation suite.

```powershell
python scripts\check_content_registry.py
```

Expected output (when all checks pass):

```
ContentRegistry loaded successfully.
  button_to_command entries: 112
  command_to_content entries: 112
  ...
  Summary: 10 passed, 0 warnings
```

---

## 5. Telegram Proxy

The bot supports an optional proxy for connecting to Telegram (e.g., via
Tor). Configure it through the `TELEGRAM_PROXY_URL` environment variable.

- **Leave it empty** (default) for a direct connection.
- **Set it** to a SOCKS5 URL to route traffic through a proxy:

  ```
  TELEGRAM_PROXY_URL=socks5h://127.0.0.1:9050
  ```

The value is read from `.env` or the system environment. No changes to
`main.py` are needed.

---

## 6. Adding or Updating Content

Edit only `data/content_items.json` to add or update content:

1. Add or update an entry in `data/content_items.json`.
2. Run `python scripts\validate_content_items.py` to verify integrity.
3. Run `python scripts\check_content_registry.py` to check the registry.
4. Restart the bot (its main loop reads the catalog on startup).

---

## Development Commands

```powershell
# Compile all Python files
python -m py_compile main.py services\content_registry.py scripts\*.py

# Run all validators
python scripts\validate_content_items.py
python scripts\check_content_registry.py
```
