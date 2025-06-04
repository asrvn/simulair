import subprocess
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

image_names = ["aaryan.png"]
image_paths = ["../../data/sample/" + image_name for image_name in image_names]

output_path = "../../models"
run_file = "../../src/Stable-Fast-3D/run.py"

resolution = "2048"

subprocess.run(["python", run_file, *image_paths, "--output-dir", output_path, "--texture-resolution", resolution])