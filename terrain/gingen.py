# python gingen.py "Dusty red canyon with sparse cacti and a shallow meandering river" -o custom_canyon.gin
'''
python -m infinigen.datagen.manage_jobs \
  --output_folder outputs/custom/canyon_scene \
  --num_scenes 1 \
  --configs custom_canyon.gin simple.gin \
  --pipeline_configs \
    local_64GB.gin \
    monocular.gin \
    cuda_terrain.gin \
    blender_gt.gin \
  --overwrite

'''
from __future__ import annotations
import os, re, json, hashlib, argparse, textwrap
from pathlib import Path
from typing import Dict, Any, Tuple

API_KEY = "AIzaSyDtHn8td2V3Nw0uxeMazdvIEV1E4stN3sE"

if not API_KEY:

    raise RuntimeError("Gemini key missing")

# --------------------------------------------------------------------------- #
# 1.  --  Parameter catalogue + ranges (ONLY nature-relevant)                 #
# --------------------------------------------------------------------------- #
Num = Tuple[type, float | int | None, float | int | None]  # (type, min, max)
PR: Dict[str, Num] = {
    "OVERALL_SEED":                              (int,  0,   None),
    "LOG_DIR":                                   (str,  None, None),
    "save_obj_and_instances.output_folder":      (str,  None, None),
    "export.output_folder":                      (str,  None, None),
    "execute_tasks.frame_range":                 (list, None, None),
    "execute_tasks.camera_id":                   (list, None, None),
    "compose_nature.terrain_enabled":            (bool, None, None),
    "compose_nature.coarse_terrain_enabled":     (bool, None, None),
    "compose_nature.terrain_surface_enabled":    (bool, None, None),
    "Terrain.main_terrain":                      (str,  None, None),
    "LandTiles.land_process":                    (str,  None, None),
    "LandTiles.randomness":                      (float,0.0, 1.0),
    "compose_nature.simulated_river_enabled":    (bool, None, None),
    "water.geo.water_height":                    (float,0.0, 0.2),
    "water.geo.with_ripples":                    (bool, None, None),
    "compose_nature.caustics_chance":            (float,0.0, 1.0),
    "compose_nature.trees_chance":               (float,0.0, 1.0),
    "compose_nature.tree_density":               (float,0.01,0.2),
    "compose_nature.bushes_chance":              (float,0.0, 1.0),
    "compose_nature.bush_density":               (float,0.0, 0.3),
    "compose_nature.grass_chance":               (float,0.0, 1.0),
    "compose_nature.flowers_chance":             (float,0.0, 1.0),
    "compose_nature.ferns_chance":               (float,0.0, 1.0),
    "compose_nature.mushroom_chance":            (float,0.0, 1.0),
    "compose_nature.cactus_chance":              (float,0.0, 1.0),
    "compose_nature.palm_trees_chance":          (float,0.0, 1.0),
    "compose_nature.coconut_trees_chance":       (float,0.0, 1.0),
    "compose_nature.instanced_trees_chance":     (float,0.0, 1.0),
    "compose_nature.boulders_chance":            (float,0.0, 1.0),
    "compose_nature.rocks_chance":               (float,0.0, 1.0),
    "compose_nature.glowing_rocks_chance":       (float,0.0, 1.0),
    "compose_nature.seashells_chance":           (float,0.0, 1.0),
    "compose_nature.ground_creatures_chance":    (float,0.0, 1.0),
    "compose_nature.max_ground_creatures":       (int,   0,   10),
    "compose_nature.flying_creatures_chance":    (float,0.0, 1.0),
    "compose_nature.fancy_clouds_chance":        (float,0.0, 1.0),
    "compose_nature.rain_particles_chance":      (float,0.0, 1.0),
    "compose_nature.snow_particles_chance":      (float,0.0, 1.0),
    "compose_nature.dust_particles_chance":      (float,0.0, 1.0),
    "populate_scene.snow_layer_chance":          (float,0.0, 1.0),
    "shader_atmosphere.density":                 (float,0.0, 0.1),
    "compose_nature.wind_chance":                (float,0.0, 1.0),
    "compose_nature.lighting_enabled":           (bool, None, None),
    "compose_nature.camera_based_lighting_chance": (float,0.0,1.0),
    "camera_selection_tags_ratio":               (dict, None, None),
    "compose_nature.inview_distance":            (float,20,  120),
    "placement.populate_all.dist_cull":          (float,20,  120),
}
PARAM_SET = set(PR)

# --------------------------------------------------------------------------- #
# 2.  --  Scene-type presets (official overrides)                             #
# --------------------------------------------------------------------------- #
PRESET: Dict[str, Dict[str, Any]] = {
    "arctic": {
        "LandTiles.land_process": "ice_erosion",
        "compose_nature.trees_chance": 0.0,
        "compose_nature.bushes_chance": 0.0,
        "compose_nature.grass_chance": 0.0,
        "compose_nature.flowers_chance": 0.0,
        "compose_nature.cactus_chance": 0.0,
        "populate_scene.snow_layer_chance": 1.0,
        "compose_nature.fancy_clouds_chance": 0.3,
        "shader_atmosphere.density": 0.0,
    },
    "canyon": {
        "Terrain.main_terrain": "CanyonTerrain",
        "LandTiles.land_process": "water_erosion",
        "compose_nature.trees_chance": 0.0,
        "compose_nature.grass_chance": 0.0,
        "compose_nature.bushes_chance": 0.1,
        "compose_nature.cactus_chance": 0.5,
        "compose_nature.rocks_chance": 0.9,
        "compose_nature.dust_particles_chance": 0.2,
    },
    "cave": {
        "compose_nature.terrain_enabled": False,
        "compose_nature.coarse_terrain_enabled": False,
        "compose_nature.trees_chance": 0.0,
        "compose_nature.grass_chance": 0.0,
        "compose_nature.glowing_rocks_chance": 0.5,
        "compose_nature.lighting_enabled": False,
        "compose_nature.camera_based_lighting_chance": 1.0,
        "compose_nature.wind_chance": 0.0,
        "compose_nature.fancy_clouds_chance": 0.0,
    },
    "cliff": {
        "Terrain.main_terrain": "CliffTerrain",
        "compose_nature.trees_chance": 0.3,
        "compose_nature.bushes_chance": 0.2,
        "compose_nature.grass_chance": 0.2,
        "compose_nature.boulders_chance": 0.9,
        "compose_nature.rocks_chance": 0.9,
    },
    "coast": {
        "water.geo.water_height": 0.04,
        "compose_nature.palm_trees_chance": 0.8,
        "compose_nature.coconut_trees_chance": 0.5,
        "compose_nature.seashells_chance": 0.5,
        "camera_selection_tags_ratio": {"liquid": (0.2, 0.5)},
        "compose_nature.fancy_clouds_chance": 0.8,
    },
    "desert": {
        "LandTiles.land_process": "wind_erosion",
        "compose_nature.trees_chance": 0.0,
        "compose_nature.bushes_chance": 0.05,
        "compose_nature.grass_chance": 0.0,
        "compose_nature.flowers_chance": 0.0,
        "compose_nature.cactus_chance": 1.0,
        "compose_nature.dust_particles_chance": 0.7,
        "compose_nature.wind_chance": 1.0,
    },
    "forest": {
        "compose_nature.trees_chance": 1.0,
        "compose_nature.tree_density": 0.11,
        "compose_nature.flowers_chance": 0.4,
        "compose_nature.ferns_chance": 0.5,
        "compose_nature.mushroom_chance": 0.3,
        "compose_nature.instanced_trees_chance": 0.8,
        "compose_nature.ground_creatures_chance": 0.2,
    },
    "mountain": {
        "Terrain.main_terrain": "RidgedTerrain",
        "compose_nature.trees_chance": 0.7,
        "compose_nature.tree_density": 0.04,
        "compose_nature.boulders_chance": 1.0,
        "compose_nature.rocks_chance": 0.9,
        "compose_nature.pinecone_chance": 0.3,
        "compose_nature.pine_needle_chance": 0.3,
    },
    "plain": {
        "compose_nature.trees_chance": 0.1,
        "compose_nature.grass_chance": 1.0,
        "compose_nature.bushes_chance": 0.4,
        "compose_nature.flowers_chance": 0.3,
    },
    "river": {
        "compose_nature.simulated_river_enabled": True,
        "water.geo.water_height": 0.02,
        "LandTiles.land_process": "water_erosion",
        "camera_selection_tags_ratio": {"liquid": (0.3, 0.7)},
    },
    "snowy mountain": {
        "Terrain.main_terrain": "HighAlpineTerrain",
        "LandTiles.land_process": "ice_erosion",
        "compose_nature.trees_chance": 0.5,
        "compose_nature.tree_density": 0.02,
        "compose_nature.snow_particles_chance": 0.7,
        "populate_scene.snow_layer_chance": 1.0,
        "compose_nature.ground_creatures_chance": 0.0,
    },
}

def preset_for(prompt: str) -> Dict[str, Any]:
    p = prompt.lower()
    for key in sorted(PRESET, key=len, reverse=True):
        if key in p:
            return PRESET[key]
    return {}

# --------------------------------------------------------------------------- #
# 3.  --  Gemini 2.0 Flash client                                             #
# --------------------------------------------------------------------------- #
from google import genai
from google.genai import types

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

# --------------------------------------------------------------------------- #
# 4.  --  Helpers                                                             #
# --------------------------------------------------------------------------- #
GIN_LINE = re.compile(r"^[\w\.]+ = .+$")

def sha_seed(txt: str) -> int:
    return int(hashlib.sha256(txt.encode()).hexdigest(), 16) & 0x7FFF_FFFF

def clamp(v: Any, lo, hi):
    if lo is None or hi is None or not isinstance(v, (int, float)):
        return v
    return max(lo, min(hi, v))

def coerce(d: Dict[str, Any]) -> Dict[str, Any]:
    fixed: Dict[str, Any] = {}
    for k, v in d.items():
        if k not in PARAM_SET:
            continue
        typ, lo, hi = PR[k]
        if typ == bool and isinstance(v, str):
            v = v.lower() in ("true", "1")
        if typ in (int, float) and isinstance(v, str) and v.replace(".", "", 1).isdigit():
            v = typ(v)
        if not isinstance(v, typ):
            continue
        fixed[k] = clamp(v, lo, hi)
    return fixed

def val2gin(v: Any) -> str:
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(val2gin(x) for x in v) + "]"
    if isinstance(v, dict):
        inner = ", ".join(f"'{k}': ({val2gin(a)}, {val2gin(b)})" for k, (a, b) in v.items())
        return "{" + inner + "}"
    return f"\"{v}\""

def dict2gin(d: Dict[str, Any]) -> str:
    return "\n".join(f"{k} = {val2gin(v)}" for k, v in sorted(d.items()))

# --------------------------------------------------------------------------- #
# 5.  --  System instruction to Gemini                                        #
# --------------------------------------------------------------------------- #
CHEATSHEET = "\n".join(f"{k} • {PR[k][0].__name__} • {PR[k][1]}–{PR[k][2]}" for k in sorted(PR))
SYS = textwrap.dedent(f"""
    You are an expert Infinigen .gin generator.
    Respond ONLY with minified JSON. Keys must be from this list (or random_seed):
    {', '.join(sorted(PARAM_SET))}
    Numeric values must stay in the given ranges.
    Do NOT output markdown or explanations.
    {CHEATSHEET}
""").strip()

# --------------------------------------------------------------------------- #
# 6.  --  Main function                                                       #
# --------------------------------------------------------------------------- #
def generate_gin(prompt: str, outfile: str = "scene.gin") -> Path:
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    base = preset_for(prompt)

    cfg = types.GenerateContentConfig(
        system_instruction=SYS,
        temperature=0.0,
        top_k=1,
        max_output_tokens=1024
    )

    resp = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=cfg
    )

    # Extract and strip any code fences
    raw = ""
    if getattr(resp, "text", None):
        raw = resp.text
    elif getattr(resp, "generations", None):
        raw = resp.generations[0].text
    raw = raw.strip()
    if raw.startswith("```"):
        # remove fence header
        raw = raw.split("\n", 1)[1]
        # remove trailing fence if present
        if raw.endswith("```"):
            raw = raw[: -3]
    raw = raw.strip()

    try:
        ai = json.loads(raw)
    except json.JSONDecodeError:
        raise RuntimeError(f"Gemini returned non-JSON:\n{raw}")

    ai = coerce(ai)
    merged = {**base, **ai}
    merged["random_seed"] = sha_seed(prompt)
    merged.setdefault("export.output_folder", Path(outfile).with_suffix("").as_posix())

    gin_text = dict2gin(merged)
    bad = [ln for ln in gin_text.splitlines() if not GIN_LINE.match(ln)]
    if bad:
        raise RuntimeError(f"Malformed gin lines: {bad}")

    Path(outfile).write_text(gin_text + "\n", encoding="utf-8")
    print(f"✅  wrote {outfile}  (params={len(merged)})")
    return Path(outfile)

# --------------------------------------------------------------------------- #
# 7.  --  CLI                                                                 #
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Text ➜ .gin for Infinigen nature scenes")
    ap.add_argument("prompt", help="Natural language terrain description")
    ap.add_argument("-o", "--outfile", default="scene.gin", help="Output .gin path")
    args = ap.parse_args()
    generate_gin(args.prompt, args.outfile)