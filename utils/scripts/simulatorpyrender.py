import trimesh
import pyrender
import numpy as np

# List of mesh file paths
mesh_files = ["../../models/aniketh/mesh.glb", "../../models/arjun/mesh.glb"]

scene = pyrender.Scene()

# Separation distance between meshes
separation = 2.0

for i, mesh_file in enumerate(mesh_files):
    # Load the mesh
    mesh = trimesh.load(mesh_file, force='mesh')

    # Apply translation to position the mesh side by side
    translation = np.array([i * separation, 0, 0])
    mesh.apply_translation(translation)

    # Create a pyrender mesh and add it to the scene
    pyrender_mesh = pyrender.Mesh.from_trimesh(mesh)
    scene.add(pyrender_mesh)

# Render the scene
pyrender.Viewer(scene, use_raymond_lighting=True)