#!/usr/bin/env python3
"""
validate_content_items.py — Audit tool for data/content_items.json.

Validates the unified content catalog in isolation.
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


def load_json(path, label):
    """Safely load a JSON file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f), None
    except FileNotFoundError:
        return None, f"{label}: file not found: {path}"
    except json.JSONDecodeError as e:
        return None, f"{label}: invalid JSON: {e}"


def main():
    warnings = []

    # ------------------------------------------------------------------
    # 1. Load content_items.json
    # ------------------------------------------------------------------
    items, err = load_json(CONTENT_ITEMS_PATH, "content_items")
    if err:
        print(f"[FAIL] {err}")
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
            print(f"        id(s) {ids} label={ascii(label)}")
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
    # 5. Missing button_label
    # ------------------------------------------------------------------
    missing_label = [i for i in items if not i.get('button_label')]
    if missing_label:
        warnings.append(f"{len(missing_label)} item(s) have missing button_label")
        print(f"[WARN]  {warnings[-1]}:")
        for item in missing_label:
            print(f"        id={item['id']}")
        print()
    else:
        print("[OK]    All items have a button_label")
        print()

    # ------------------------------------------------------------------
    # 6. Missing command_key
    # ------------------------------------------------------------------
    missing_cmd = [i for i in items if not i.get('command_key')]
    if missing_cmd:
        warnings.append(f"{len(missing_cmd)} item(s) have missing command_key")
        print(f"[WARN]  {warnings[-1]}:")
        for item in missing_cmd:
            print(f"        id={item['id']}")
        print()
    else:
        print("[OK]    All items have a command_key")
        print()

    # ------------------------------------------------------------------
    # 7. Missing channel_key for active items
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
    # 8. Empty message_ids for active items
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
    # 9. All message_ids are integers (not strings, floats, etc.)
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
    # 10. Summary
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
