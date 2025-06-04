import dearpygui.dearpygui as dpg
import subprocess
import threading
import time

def nvidia_smi():

    try:

        result = subprocess.run(['nvidia-smi'], stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
        return result.stdout if result.returncode == 0 else result.stderr

    except Exception as e:

        return str(e)

def update_output():

    while True:

        output = nvidia_smi()
        dpg.set_value('nvidia_smi_text', output)
        time.sleep(1)

dpg.create_context()

with dpg.window(label = "NVIDIA SMI Monitor", width = 800, height = 600):

    dpg.add_text(default_value = "Fetching NVIDIA SMI data...", tag = 'nvidia_smi_text')

dpg.create_viewport(title='NVIDIA SMI Monitor', width = 800, height = 600)
dpg.setup_dearpygui()

thread = threading.Thread(target = update_output, daemon = True)
thread.start()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

# Anieesh Saravanan, 3, 2025