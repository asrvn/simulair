import torch
print("Library imported")

def cuda_enabled():

    print("Function executed")

    if torch.cuda.is_available():

        print("CUDA is available")

        print("GPU: ", torch.cuda.get_device_name(0))

    else:

        print("CUDA is not available")

cuda_enabled()

# Anieesh Saravanan, 3, 2025