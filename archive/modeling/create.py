import subprocess
import os
import time

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

image_names = []
image_paths = ["data/sample/" + image_name for image_name in image_names]

output_path = "models"
run_file = "src/Stable-Fast-3D/run.py"

start = time.time()

# Suppress warnings by setting the PYTHONWARNINGS environment variable
result = subprocess.run(["python", run_file, *image_paths, "--output-dir", output_path],
                        text = True,
                        capture_output = True,
                        env = dict(os.environ, PYTHONWARNINGS = "ignore"))

elapsed = time.time() - start

print(f"Elapsed time: {elapsed:.2f} s")
print(result.stdout)

# Anieesh Saravanan, 3, 2025