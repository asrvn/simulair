import pyrender
import trimesh

modoel = trimesh.load('../../models/aniketh/mesh.glb')

if isinstance(modoel, trimesh.Scene):

    meshes = [trimesh.Trimesh(vertices = mesh.vertices, faces = mesh.faces) for mesh in modoel.geometry.values()]

else:

    meshes = [modoel]

pyrender_meshes = [pyrender.Mesh.from_trimesh(mesh) for mesh in meshes]
scene = pyrender.Scene()

for mesh in pyrender_meshes:

    scene.add(mesh)

pyrender.Viewer(scene, use_raymond_lighting = True)

# Anieesh Saravanan, 3, 2025