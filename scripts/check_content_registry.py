#!/usr/bin/env python3
"""
check_content_registry.py — Smoke-test for ContentRegistry.

Imports ContentRegistry, instantiates it, prints basic stats,
and runs validation.
"""

import sys
import os.path as _osp

# Ensure project root is on sys.path so the services package is importable
_script_dir = _osp.dirname(_osp.abspath(__file__))
_project_root = _osp.abspath(_osp.join(_script_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from services.content_registry import ContentRegistry


def main():
    registry = ContentRegistry()

    if registry.load_error:
        print(f"ERROR: {registry.load_error}")
        sys.exit(1)

    # Basic stats
    btn_count = len(registry.button_to_command)
    cmd_count = len(registry.command_to_content)
    print(f"ContentRegistry loaded successfully.")
    print(f"  button_to_command entries: {btn_count}")
    print(f"  command_to_content entries: {cmd_count}")
    print()

    # Quick spot-checks (use command_key for console-safe output)
    sample_label = list(registry.button_to_command.keys())[0]
    sample_cmd = registry.get_command_for_button(sample_label)
    print(f"  Sample lookup: first label -> {sample_cmd!r}")
    sample_content = registry.get_content_for_command(sample_cmd)
    if sample_content:
        print(f"  Content item keys: {list(sample_content.keys())}")
        print(f"  message_ids: {sample_content.get('message_ids')}")
        print(f"  channel_key: {sample_content.get('channel_key')}")
    print()

    # Validation
    registry.print_validation_report()


if __name__ == '__main__':
    main()
