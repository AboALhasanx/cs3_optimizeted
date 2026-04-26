#!/usr/bin/env python3
"""
validate_content_maps.py — Audit tool for cs3 JSON mapping files.

Validates the legacy btn2cmd and cmd2values JSON files (now in legacy/).
These files are kept for historical reference and are not used at runtime.
This is a read-only audit; it always exits 0.

Usage:
    python scripts/validate_content_maps.py
"""

import json
import sys
from collections import Counter

# ---------------------------------------------------------------------------
# Resolve paths via app_paths (add project root to sys.path so the import
# works even when this script is launched from the scripts/ directory).
# ---------------------------------------------------------------------------
import os.path as _osp
_script_dir = _osp.dirname(_osp.abspath(__file__))
_project_root = _osp.abspath(_osp.join(_script_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

BTN2CMD_PATH = _osp.join(_project_root, 'legacy', 'cs3_terms_btn2cmd.json')
CMD2VALUES_PATH = _osp.join(_project_root, 'legacy', 'cs3_terms_cmd2values.json')


def load_json(path, label):
    """Safely load a JSON file and return (data, error_message_or_None)."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f), None
    except FileNotFoundError:
        return None, f"{label}: file not found: {path}"
    except json.JSONDecodeError as e:
        return None, f"{label}: invalid JSON: {e}"


def main():
    errors = []
    warnings = []

    # ---- 1. Load files ----------------------------------------------------
    btn2cmd, err = load_json(BTN2CMD_PATH, "btn2cmd")
    if err:
        print(f"[FAIL] {err}")
        sys.exit(0)  # still exit 0 per spec

    cmd2values, err = load_json(CMD2VALUES_PATH, "cmd2values")
    if err:
        print(f"[FAIL] {err}")
        sys.exit(0)

    # ---- 2. Extract data structures ---------------------------------------
    commands = cmd2values.get('commands', {})
    if not isinstance(commands, dict):
        print("[FAIL] cmd2values['commands'] is not a dict")
        sys.exit(0)

    # ---- 3. Counts --------------------------------------------------------
    btn_count = len(btn2cmd)
    cmd_count = len(commands)
    print(f"btn2cmd entries  (button -> command_key):  {btn_count}")
    print(f"cmd2values entries (command_key -> ids):    {cmd_count}")
    print()

    # ---- 4. Buttons whose command_key is missing from commands -------------
    missing_commands = []
    for btn_text, cmd_key in btn2cmd.items():
        if cmd_key not in commands:
            missing_commands.append((btn_text, cmd_key))

    if missing_commands:
        warnings.append(
            f"{len(missing_commands)} button(s) reference a command_key "
            f"missing from cmd2values['commands']"
        )
        print(f"[WARN]  {warnings[-1]}:")
        for btn_text, cmd_key in missing_commands:
            print(f"        button  = {btn_text!r}")
            print(f"        command = {cmd_key!r}")
        print()
    else:
        print("[OK]    All button command_keys exist in cmd2values['commands']")
        print()

    # ---- 5. Commands with null value --------------------------------------
    null_commands = [k for k, v in commands.items() if v is None]
    if null_commands:
        warnings.append(f"{len(null_commands)} command(s) have null value")
        print(f"[WARN]  {warnings[-1]}:")
        for k in null_commands:
            print(f"        {k!r}")
        print()
    else:
        print("[OK]    No commands have null value")
        print()

    # ---- 6. Commands with empty list value --------------------------------
    empty_commands = [k for k, v in commands.items()
                      if isinstance(v, list) and len(v) == 0]
    if empty_commands:
        warnings.append(f"{len(empty_commands)} command(s) have empty list value")
        print(f"[WARN]  {warnings[-1]}:")
        for k in empty_commands:
            print(f"        {k!r}")
        print()
    else:
        print("[OK]    No commands have an empty list value")
        print()

    # ---- 7. Duplicate command values in btn2cmd ---------------------------
    cmd_key_counts = Counter(btn2cmd.values())
    duplicates = {k: v for k, v in cmd_key_counts.items() if v > 1}
    if duplicates:
        warnings.append(
            f"{len(duplicates)} command_key(s) are mapped from multiple buttons"
        )
        print(f"[WARN]  {warnings[-1]}:")
        for cmd_key, count in sorted(duplicates.items()):
            buttons = [b for b, c in btn2cmd.items() if c == cmd_key]
            print(f"        {cmd_key!r} appears {count}x → {buttons}")
        print()
    else:
        print("[OK]    No duplicate command_keys in btn2cmd")
        print()

    # ---- 8. Summary -------------------------------------------------------
    print("=" * 55)
    print("SUMMARY")
    print("=" * 55)
    print(f"  buttons in btn2cmd:            {btn_count}")
    print(f"  commands in cmd2values:        {cmd_count}")
    print(f"  warnings:                      {len(warnings)}")
    print(f"  fatal errors:                  {len(errors)}")
    if warnings:
        print()
        for w in warnings:
            print(f"  [!] {w}")
    print()
    print("Exit code: 0 (audit only, no blockers)")
    print()

    sys.exit(0)


if __name__ == '__main__':
    main()
