# app_paths.py
# Project-relative path constants for data files.
# This replaces hardcoded Android paths in main.py.

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Active (current) JSON mapping files
CMD2VALUES_PATH = os.path.join(BASE_DIR, 'cs3_terms_cmd2values.json')
BTN2CMD_PATH = os.path.join(BASE_DIR, 'cs3_terms_btn2cmd.json')
