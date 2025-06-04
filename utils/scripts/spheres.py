import trimesh
import pyrender
import numpy as np

scene = pyrender.Scene()

tm = trimesh.load("../../models/aniketh/mesh.glb", force='mesh')

# https://github.com/KhronosGroup/glTF/tree/main/specification/2.0#materials
mesh = pyrender.Mesh.from_trimesh(tm)
# mesh = pyrender.Mesh.from_trimesh(mesh, material=pyrender.MetallicRoughnessMaterial())
# mesh = pyrender.Mesh.from_trimesh(mesh, smooth=False)

pts = tm.vertices.copy()
sm = trimesh.creation.uv_sphere(radius=0.005)
sm.visual.vertex_colors = [1.0, 0.0, 0.0]
tfs = np.tile(np.eye(4), (len(pts), 1, 1))
tfs[:,:3,3] = pts
m = pyrender.Mesh.from_trimesh(sm, poses=tfs)

# scene.add(mesh)
scene.add(m)
pyrender.Viewer(scene, use_raymond_lighting=True)