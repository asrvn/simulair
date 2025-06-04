"""
Recursively convert GLB files to usdc format using Blender.

Usage:
    blender --background --python glb_to_usdc.py -- <input_folder>
"""

import sys
from pathlib import Path
import bpy

# ── INPUT HANDLING ───────────────────────────────────────────────────────────
def get_input_folder():
    """
    Retrieve the input folder from command-line arguments.
    Ignore Blender flags (starting with '-') and the script filename,
    taking the first remaining argument as the folder path.
    """
    args = sys.argv[1:]
    candidates = [arg for arg in args if not arg.startswith('-') and not arg.lower().endswith('.py')]
    if not candidates:
        print("Usage: blender --background --python glb_to_usdc_batch.py -- <input_folder>")
        sys.exit(1)

    folder = Path(candidates[0]).resolve()
    if not folder.is_dir():
        print(f"Error: Input folder does not exist or is not a directory: {folder}")
        sys.exit(1)

    return folder

# ── SCENE CLEANUP ────────────────────────────────────────────────────────────
def clear_scene():
    """
    Delete all objects in the scene and purge orphans for a clean state.
    """
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

# ── IMPORT & EXPORT ─────────────────────────────────────────────────────────
def import_glb(filepath: Path):
    """
    Import a GLB file into the current Blender scene.
    """
    bpy.ops.import_scene.gltf(filepath=str(filepath))


def export_usdc(filepath: Path):
    """
    Export the current Blender scene to a usdc file.
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.usd_export(filepath=str(filepath))

# ── FILE DISCOVERY ──────────────────────────────────────────────────────────
def find_glb_files(root: Path):
    """
    Recursively find all .glb files under the root folder (case-insensitive).
    """
    return [p for p in root.rglob('*') if p.is_file() and p.suffix.lower() == '.glb']

# ── BATCH CONVERSION ─────────────────────────────────────────────────────────
def convert_folder(input_folder: Path):
    """
    Convert all found GLB files to usdc format, skipping existing outputs.
    """
    glb_files = find_glb_files(input_folder)
    total = len(glb_files)
    converted = skipped = 0

    if total == 0:
        print(f"No .glb files found in '{input_folder}'.")
        return

    for idx, glb in enumerate(glb_files, start=1):
        usdc = glb.with_suffix('.usdc')
        print(f"[{idx}/{total}]", end=' ')
        if usdc.exists():
            print(f"Skipping existing: {usdc}")
            skipped += 1
            continue

        print(f"Converting: {glb} -> {usdc}")
        clear_scene()
        try:
            import_glb(glb)
            export_usdc(usdc)
            converted += 1
        except Exception as e:
            print(f"Error converting '{glb}': {e}", file=sys.stderr)

    print(f"Conversion complete. Total: {total}, Converted: {converted}, Skipped: {skipped}")

# ── ENTRY POINT ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # Ensure Blender stops parsing flags before our script arguments
    folder = get_input_folder()
    convert_folder(folder)
