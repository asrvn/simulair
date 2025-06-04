from queue import Queue
import subprocess
import time

def nvidia_smi():

    command = "nvidia-smi --query-gpu=index,name,utilization.gpu,temperature.gpu,memory.used,memory.total --format=csv,noheader,nounits".split()
    process = subprocess.Popen(command,
                               stdout = subprocess.PIPE,
                               stderr = subprocess.PIPE,
                               text = True)

    data = Queue()

    while True:

        if not (line := process.stdout.readline().strip()):

            break

        data.put(line)

    return data

# Anieesh Saravanan, 3, 2025