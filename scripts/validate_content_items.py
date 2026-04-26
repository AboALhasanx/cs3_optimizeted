#!/usr/bin/env python3
"""
validate_content_items.py — Audit tool for data/content_items.json.

Reads the new unified content catalog and cross-checks it against the
original cs3_terms_btn2cmd.json and cs3_terms_cmd2values.json files
(now located in the legacy/ directory).
This is a read-only audit; it always exits 0.

Usage:
    python scripts/validate_content_items.py
"""

import json
import sys
import os.path as _osp

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
_script_dir = _osp.dirname(_osp.abspath(__file__))
_project_root = _osp.abspath(_osp.join(_script_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

CONTENT_ITEMS_PATH = _osp.join(_project_root, 'data', 'content_items.json')
BTN2CMD_PATH = _osp.join(_project_root, 'legacy', 'cs3_terms_btn2cmd.json')
CMD2VALUES_PATH = _osp.join(_project_root, 'legacy', 'cs3_terms_cmd2values.json')


def load_json(path, label):
    """Safely load a JSON file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f), None
    except FileNotFoundError:
        return None, f"{label}: file not found: {path}"
    except json.JSONDecodeError as e:
        return None, f"{label}: invalid JSON: {e}"


def normalize_ids(value):
    """Convert a scalar int to a single-element list; keep lists as-is."""
    if isinstance(value, int):
        return [value]
    if isinstance(value, list):
        return value
    return []


def main():
    warnings = []

    # ------------------------------------------------------------------
    # 1. Load all three files
    # ------------------------------------------------------------------
    items, err = load_json(CONTENT_ITEMS_PATH, "content_items")
    if err:
        print(f"[FAIL] {err}")
        sys.exit(0)

    btn2cmd, err = load_json(BTN2CMD_PATH, "btn2cmd")
    if err:
        print(f"[FAIL] {err}")
        sys.exit(0)

    cmd2values, err = load_json(CMD2VALUES_PATH, "cmd2values")
    if err:
        print(f"[FAIL] {err}")
        sys.exit(0)

    commands = cmd2values.get('commands', {})
    if not isinstance(commands, dict):
        print("[FAIL] cmd2values['commands'] is not a dict")
        sys.exit(0)

    # ------------------------------------------------------------------
    # 2. Basic counts
    # ------------------------------------------------------------------
    total = len(items)
    active = [i for i in items if i.get('active', False)]
    inactive = [i for i in items if not i.get('active', False)]
    print(f"content_items total:   {total}")
    print(f"  active:              {len(active)}")
    print(f"  inactive:            {len(inactive)}")
    print()

    # ------------------------------------------------------------------
    # 3. Duplicate button_label
    # ------------------------------------------------------------------
    seen_labels = {}
    for item in items:
        label = item.get('button_label')
        if label in seen_labels:
            seen_labels[label].append(item['id'])
        else:
            seen_labels[label] = [item['id']]
    dup_labels = {k: v for k, v in seen_labels.items() if len(v) > 1}
    if dup_labels:
        warnings.append(f"{len(dup_labels)} duplicate button_label(s)")
        print(f"[WARN]  {warnings[-1]}:")
        for label, ids in sorted(dup_labels.items()):
            print(f"        {label!r} appears in ids {ids}")
        print()
    else:
        print("[OK]    No duplicate button_labels")
        print()

    # ------------------------------------------------------------------
    # 4. Duplicate command_key
    # ------------------------------------------------------------------
    seen_cmds = {}
    for item in items:
        cmd = item.get('command_key')
        if cmd in seen_cmds:
            seen_cmds[cmd].append(item['id'])
        else:
            seen_cmds[cmd] = [item['id']]
    dup_cmds = {k: v for k, v in seen_cmds.items() if len(v) > 1}
    if dup_cmds:
        warnings.append(f"{len(dup_cmds)} duplicate command_key(s)")
        print(f"[WARN]  {warnings[-1]}:")
        for cmd, ids in sorted(dup_cmds.items()):
            print(f"        {cmd!r} appears in ids {ids}")
        print()
    else:
        print("[OK]    No duplicate command_keys")
        print()

    # ------------------------------------------------------------------
    # 5. Missing channel_key for active items
    # ------------------------------------------------------------------
    missing_channel = [i for i in active if not i.get('channel_key')]
    if missing_channel:
        warnings.append(
            f"{len(missing_channel)} active item(s) have missing channel_key"
        )
        print(f"[WARN]  {warnings[-1]}:")
        for item in missing_channel:
            print(f"        id={item['id']} cmd={item['command_key']!r}")
        print()
    else:
        print("[OK]    All active items have a channel_key")
        print()

    # ------------------------------------------------------------------
    # 6. Empty message_ids for active items
    # ------------------------------------------------------------------
    empty_ids = [i for i in active if not i.get('message_ids')]
    if empty_ids:
        warnings.append(
            f"{len(empty_ids)} active item(s) have empty message_ids"
        )
        print(f"[WARN]  {warnings[-1]}:")
        for item in empty_ids:
            print(f"        id={item['id']} cmd={item['command_key']!r}")
        print()
    else:
        print("[OK]    All active items have non-empty message_ids")
        print()

    # ------------------------------------------------------------------
    # 7. All message_ids are integers (not strings, floats, etc.)
    # ------------------------------------------------------------------
    bad_ids = []
    for item in active:
        for mid in item.get('message_ids', []):
            if not isinstance(mid, int):
                bad_ids.append((item['id'], item['command_key'], mid))
    if bad_ids:
        warnings.append(
            f"{len(bad_ids)} non-integer message_id(s) found in active items"
        )
        print(f"[WARN]  {warnings[-1]}:")
        for item_id, cmd, mid in bad_ids:
            print(f"        id={item_id} cmd={cmd!r} value={mid!r}")
        print()
    else:
        print("[OK]    All message_ids are integers")
        print()

    # ------------------------------------------------------------------
    # 8. Cross-check: button labels match btn2cmd keys
    # ------------------------------------------------------------------
    btn2cmd_labels = set(btn2cmd.keys())
    content_labels = set(i['button_label'] for i in items)

    missing_labels = btn2cmd_labels - content_labels
    extra_labels = content_labels - btn2cmd_labels
    if missing_labels:
        warnings.append(
            f"{len(missing_labels)} label(s) in btn2cmd missing from content_items"
        )
        print(f"[WARN]  {warnings[-1]}:")
        for lbl in sorted(missing_labels):
            print(f"        {lbl!r}")
        print()
    if extra_labels:
        warnings.append(
            f"{len(extra_labels)} label(s) in content_items not in btn2cmd"
        )
        print(f"[WARN]  {warnings[-1]}:")
        for lbl in sorted(extra_labels):
            print(f"        {lbl!r}")
        print()
    if not missing_labels and not extra_labels:
        print("[OK]    All button_labels match btn2cmd")
        print()

    # ------------------------------------------------------------------
    # 9. Cross-check: command keys match btn2cmd values
    # ------------------------------------------------------------------
    btn2cmd_commands = set(btn2cmd.values())
    content_commands = set(i['command_key'] for i in items)

    missing_cmds = btn2cmd_commands - content_commands
    extra_cmds = content_commands - btn2cmd_commands
    if missing_cmds:
        warnings.append(
            f"{len(missing_cmds)} command_key(s) in btn2cmd missing from "
            f"content_items"
        )
        print(f"[WARN]  {warnings[-1]}:")
        for cmd in sorted(missing_cmds):
            print(f"        {cmd!r}")
        print()
    if extra_cmds:
        warnings.append(
            f"{len(extra_cmds)} command_key(s) in content_items not in btn2cmd"
        )
        print(f"[WARN]  {warnings[-1]}:")
        for cmd in sorted(extra_cmds):
            print(f"        {cmd!r}")
        print()
    if not missing_cmds and not extra_cmds:
        print("[OK]    All command_keys match btn2cmd")
        print()

    # ------------------------------------------------------------------
    # 10. Cross-check: message IDs match cmd2values (normalized)
    # ------------------------------------------------------------------
    mismatched_ids = []
    for item in active:
        cmd = item['command_key']
        expected_raw = commands.get(cmd)
        if expected_raw is None:
            mismatched_ids.append((item['id'], cmd, 'missing_from_cmd2values', []))
            continue

        expected_ids = normalize_ids(expected_raw)
        actual_ids = item.get('message_ids', [])

        # Sort both for comparison since order might differ
        if sorted(actual_ids) != sorted(expected_ids):
            mismatched_ids.append((item['id'], cmd, expected_ids, actual_ids))

    if mismatched_ids:
        warnings.append(
            f"{len(mismatched_ids)} item(s) with message_ids mismatch"
        )
        print(f"[WARN]  {warnings[-1]}:")
        for item_id, cmd, expected, actual in mismatched_ids:
            print(f"        id={item_id} cmd={cmd!r}")
            print(f"          expected={expected}")
            print(f"          actual  ={actual}")
        print()
    else:
        print("[OK]    All message_ids match cmd2values (after normalization)")
        print()

    # ------------------------------------------------------------------
    # 11. Summary
    # ------------------------------------------------------------------
    print("=" * 55)
    print("SUMMARY")
    print("=" * 55)
    print(f"  content_items total:               {total}")
    print(f"  active / inactive:                 {len(active)} / {len(inactive)}")
    print(f"  warnings:                          {len(warnings)}")
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
