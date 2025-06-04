from rembg import remove
from PIL import Image

def remove_background(path):

    input = Image.open(path)
    output = remove(input)

    return output

# Anieesh Saravanan, 3, 2025