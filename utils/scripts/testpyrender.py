import numpy as np
import pyrender
import trimesh

# Load the scene and mesh
scene = pyrender.Scene(bg_color=[0, 0, 0])

base = trimesh.load("../../models/aniketh/mesh.glb", force='mesh')

# Apply a rotation to align the model to the x-z plane
# 90 degrees rotation around the x-axis
rotation_matrix = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

# Create a mesh with the new material
mesh = pyrender.Mesh.from_trimesh(base)

# Add the mesh to the scene with the rotation applied
scene.add(mesh, pose=rotation_matrix)

# Render the scene with lighting
pyrender.Viewer(scene, run_in_thread=True, use_raymond_lighting=True)
