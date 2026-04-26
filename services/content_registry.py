#!/usr/bin/env python3
"""
content_registry.py — Service that reads the unified content catalog.

Provides dict-based lookups (button_label -> command_key,
command_key -> content item) and validation helpers.

Usage:
    from services.content_registry import ContentRegistry
    registry = ContentRegistry()
    cmd = registry.get_command_for_button("some button text")
    content = registry.get_content_for_command("some_command")
    registry.print_validation_report()
"""

import json
import os


class ContentRegistry:
    """Read-only registry backed by data/content_items.json."""

    # Default path relative to this file's location
    _CONTENT_ITEMS_REL = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', 'data', 'content_items.json'
    )

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------
    def __init__(self, file_path=None):
        """
        :param file_path: Optional explicit path to content_items.json.
                          Falls back to the default location relative to
                          this file.
        """
        self._file_path = file_path or self._CONTENT_ITEMS_REL
        self._items = []
        self._button_to_command = {}
        self._command_to_content = {}
        self._loaded = False
        self._load_error = None

        self._load()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _load(self):
        """Load and index content_items.json."""
        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                self._items = json.load(f)
        except FileNotFoundError:
            self._load_error = f"File not found: {self._file_path}"
            self._items = []
        except json.JSONDecodeError as e:
            self._load_error = f"Invalid JSON in {self._file_path}: {e}"
            self._items = []

        # Build lookup dicts (include both active and inactive)
        self._button_to_command = {}
        self._command_to_content = {}
        for item in self._items:
            label = item.get('button_label')
            cmd = item.get('command_key')
            if label:
                self._button_to_command[label] = cmd
            if cmd:
                self._command_to_content[cmd] = item

        self._loaded = True

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------
    @property
    def items(self):
        """All content items (list of dicts)."""
        return list(self._items)

    @property
    def active_items(self):
        """Only items where active is truthy."""
        return [i for i in self._items if i.get('active', False)]

    @property
    def inactive_items(self):
        """Only items where active is falsy."""
        return [i for i in self._items if not i.get('active', False)]

    @property
    def button_to_command(self):
        """dict mapping button_label -> command_key (all items)."""
        return dict(self._button_to_command)

    @property
    def command_to_content(self):
        """dict mapping command_key -> content item dict (all items)."""
        return dict(self._command_to_content)

    @property
    def load_error(self):
        """Error message from the last load attempt, or None."""
        return self._load_error

    @property
    def loaded(self):
        """True if the file was loaded (even if empty)."""
        return self._loaded

    # ------------------------------------------------------------------
    # Lookup methods
    # ------------------------------------------------------------------
    def get_command_for_button(self, button_text):
        """
        Return the command_key associated with *button_text*,
        or None if not found.
        """
        return self._button_to_command.get(button_text)

    def get_content_for_command(self, command_key):
        """
        Return the full content item dict for *command_key*,
        or None if not found.
        """
        return self._command_to_content.get(command_key)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def validate(self):
        """
        Run integrity checks on active items only.

        Returns a list of (severity, message) tuples.
        Severity is one of "OK", "WARN".
        """
        results = []
        active = self.active_items

        # -- helper to add a result ------------------------------------
        def ok(msg):
            results.append(("OK", msg))

        def warn(msg):
            results.append(("WARN", msg))

        # 1. Counts
        ok(f"Total items: {len(self._items)}")
        ok(f"Active items: {len(active)}")
        ok(f"Inactive items: {len(self.inactive_items)}")

        # 2. Duplicate button_label (active only)
        seen_labels = {}
        for item in active:
            lbl = item.get('button_label')
            seen_labels.setdefault(lbl, []).append(item['id'])
        dup_labels = {k: v for k, v in seen_labels.items() if len(v) > 1}
        if dup_labels:
            for lbl, ids in dup_labels.items():
                safe_lbl = ascii(lbl) if any(ord(c) > 127 for c in lbl) else lbl
                warn(f"Duplicate button_label {safe_lbl} in ids {ids}")
        else:
            ok("No duplicate button_labels among active items")

        # 3. Duplicate command_key (active only)
        seen_cmds = {}
        for item in active:
            cmd = item.get('command_key')
            seen_cmds.setdefault(cmd, []).append(item['id'])
        dup_cmds = {k: v for k, v in seen_cmds.items() if len(v) > 1}
        if dup_cmds:
            for cmd, ids in dup_cmds.items():
                warn(f"Duplicate command_key {cmd!r} in ids {ids}")
        else:
            ok("No duplicate command_keys among active items")

        # 4. Missing button_label
        missing_label = [i for i in active if not i.get('button_label')]
        if missing_label:
            for item in missing_label:
                warn(f"Missing button_label in id={item['id']}")
        else:
            ok("All active items have a button_label")

        # 5. Missing command_key
        missing_cmd = [i for i in active if not i.get('command_key')]
        if missing_cmd:
            for item in missing_cmd:
                warn(f"Missing command_key in id={item['id']}")
        else:
            ok("All active items have a command_key")

        # 6. Missing channel_key
        missing_ch = [i for i in active if not i.get('channel_key')]
        if missing_ch:
            for item in missing_ch:
                warn(f"Missing channel_key in id={item['id']} "
                     f"cmd={item.get('command_key', '?')!r}")
        else:
            ok("All active items have a channel_key")

        # 7. Empty message_ids
        empty = [i for i in active if not i.get('message_ids')]
        if empty:
            for item in empty:
                warn(f"Empty message_ids in id={item['id']} "
                     f"cmd={item.get('command_key', '?')!r}")
        else:
            ok("All active items have non-empty message_ids")

        # 8. Non-integer message_ids
        bad_ids = []
        for item in active:
            for mid in item.get('message_ids', []):
                if not isinstance(mid, int):
                    bad_ids.append((item['id'], item.get('command_key', '?'), mid))
        if bad_ids:
            for item_id, cmd, mid in bad_ids:
                warn(f"Non-integer message_id in id={item_id} "
                     f"cmd={cmd!r} value={mid!r}")
        else:
            ok("All message_ids are integers")

        return results

    def print_validation_report(self):
        """Print a formatted validation report to stdout."""
        print("=" * 60)
        print("  ContentRegistry Validation Report")
        print("=" * 60)
        if self._load_error:
            print(f"\n  [LOAD ERROR] {self._load_error}\n")
            return

        results = self.validate()
        warn_count = sum(1 for sev, _ in results if sev == "WARN")
        ok_count = sum(1 for sev, _ in results if sev == "OK")

        for severity, message in results:
            prefix = "[OK]" if severity == "OK" else "[WARN]"
            print(f"  {prefix}  {message}")

        print()
        print(f"  Summary: {ok_count} passed, {warn_count} warnings")
        print("=" * 60)
