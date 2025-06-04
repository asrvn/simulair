import subprocess
import time
import f3d
import os

def toggle_omp_warning():

    if "KMP_DUPLICATE_LIB_OK" in os.environ:

        del os.environ["KMP_DUPLICATE_LIB_OK"]

    else:

        os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def generate_model(image_paths, output_path):

    run_file = "../src/Stable-Fast-3D/run.py"

    start = time.time()

    # Suppress warnings by setting the PYTHONWARNINGS environment variable
    result = subprocess.run(["python", run_file, *image_paths, "--output-dir", output_path],
                            text = True,
                            capture_output = True,
                            env = dict(os.environ, PYTHONWARNINGS = "ignore"))

    elapsed = time.time() - start

    return {"time" : elapsed, "output" : result.stdout.replace("  ", " ").split("\n")[:-1]}

def render_model(model_path):

    f3d.Engine.autoload_plugins()  # Load static plugins
    eng = f3d.Engine(f3d.Window.NATIVE)  # Create a native window engine

    try:

        eng.loader.load_scene(model_path)

    except RuntimeError as e:

        print(e)

    eng.window.render()
    eng.interactor.start()

a = generate_model(["tree.png"], "output")
print(a)

# Anieesh Saravanan, 3, 2025