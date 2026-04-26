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
│   ├── validate_content_maps.py      ← Validates old JSON maps
│   └── check_content_registry.py     ← Smoke-test for ContentRegistry
├── legacy/
│   ├── cs3_terms_btn2cmd.json        ← Old map (archived, validation)
│   ├── cs3_terms_cmd2values.json     ← Old map (archived, validation)
│   ├── terms_btn2cmd.json            ← CRLF duplicate (archive only)
│   └── terms_cmd2values.json         ← CRLF duplicate (archive only)
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

---

## 3. Legacy JSON Maps (Archived, Validation Only)

All old mapping files now live in the `legacy/` directory. They are
**not** read by the running bot; they are kept for historical reference
and cross-validation.

- `legacy/cs3_terms_btn2cmd.json` — maps button labels → command keys
- `legacy/cs3_terms_cmd2values.json` — maps command keys → message IDs
- `legacy/terms_btn2cmd.json` — CRLF duplicate of the above (archive)
- `legacy/terms_cmd2values.json` — CRLF duplicate of the above (archive)

The `cs3_terms_*` files contain the same logical data as the `terms_*`
files; they differ only in line endings (LF vs. CRLF).

---

## 4. Validation: New Catalog vs. Legacy Maps

**`scripts/validate_content_items.py`** is the primary validation tool.

It loads `data/content_items.json` and cross-checks it against the
legacy `legacy/cs3_terms_btn2cmd.json` and
`legacy/cs3_terms_cmd2values.json` files:

- Verifies every button label matches
- Verifies every command key matches
- Verifies every message ID matches (after normalising scalars to lists)
- Checks for duplicates, nulls, empty lists, and missing fields

Run it with:

```powershell
python scripts\validate_content_items.py
```

---

## 5. Validation: Legacy Maps Only

**`scripts/validate_content_maps.py`** validates the legacy
`legacy/cs3_terms_btn2cmd.json` and `legacy/cs3_terms_cmd2values.json`
files independently. It checks for:

- Orphaned command keys
- Null or empty-list values
- Duplicate command mappings

This script remains useful as long as the old files are kept. Run it
with:

```powershell
python scripts\validate_content_maps.py
```

---

## 6. Smoke-Test for ContentRegistry

**`scripts/check_content_registry.py`** is a quick health-check that
instantiates `ContentRegistry`, loads the catalog, and runs the full
validation suite.

```powershell
python scripts\check_content_registry.py
```

Expected output (when all checks pass):

```
ContentRegistry loaded successfully.
  button_to_command entries: 110
  command_to_content entries: 110
  ...
  Summary: 10 passed, 0 warnings
```

---

## 6. Telegram Proxy

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

## 7. Adding or Updating Content

**Do not** edit the legacy JSON files in the `legacy/` directory
for new content. Instead:

1. Add or update an entry in `data/content_items.json`.
2. Run `python scripts\validate_content_items.py` to verify integrity.
3. Run `python scripts\check_content_registry.py` to check the registry.
4. Restart the bot (its main loop reads the catalog on startup).

This ensures that `data/content_items.json` remains the single point of
truth and the old JSON files are only used for validation comparison.

---

## Development Commands

```powershell
# Compile all Python files
python -m py_compile main.py services\content_registry.py scripts\*.py

# Run all validators
python scripts\validate_content_items.py
python scripts\validate_content_maps.py
python scripts\check_content_registry.py
```
