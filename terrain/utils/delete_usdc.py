#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
delete_usdc_batch.py — Recursively delete usdc files within a directory.

Usage:
    python delete_usdc.py <input_folder>

This script searches the input folder and its subdirectories for files ending in
.usdc or .usdc and deletes each one. Progress and summary are printed to stdout.
"""

import sys
from pathlib import Path

# ── INPUT HANDLING ───────────────────────────────────────────────────────────
def get_input_folder():
    """
    Retrieve the input folder from command-line arguments.
    """
    if len(sys.argv) != 2:
        print("Usage: python delete_usdc_batch.py <input_folder>")
        sys.exit(1)

    folder = Path(sys.argv[1]).resolve()
    if not folder.is_dir():
        print(f"Error: Input folder does not exist or is not a directory: {folder}")
        sys.exit(1)

    return folder

# ── FILE DISCOVERY ──────────────────────────────────────────────────────────
def find_usdc_files(root: Path):
    """
    Recursively find all .usdc files under the root folder (case-insensitive).
    """
    return [p for p in root.rglob('*') if p.is_file() and p.suffix.lower() == '.usdc']

# ── DELETION ────────────────────────────────────────────────────────────────
def delete_usdc_files(files):
    """
    Delete each file in the provided list, printing progress.
    """
    total = len(files)
    for idx, file in enumerate(files, start=1):
        print(f"[{idx}/{total}] Deleting: {file}")
        try:
            file.unlink()
        except Exception as e:
            print(f"Error deleting '{file}': {e}", file=sys.stderr)

# ── ENTRY POINT ─────────────────────────────────────────────────────────────
def main():
    folder = get_input_folder()
    usdc_files = find_usdc_files(folder)

    if not usdc_files:
        print(f"No .usdc files found in '{folder}'.")
        return

    delete_usdc_files(usdc_files)
    print(f"Deletion complete. Total deleted: {len(usdc_files)}")

if __name__ == '__main__':
    main()
