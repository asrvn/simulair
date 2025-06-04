import trimesh
import pyvista as pv
import numpy as np
from PIL import Image

scene_or_mesh = trimesh.load('../../models/aniketh/mesh.glb')

# Initialize lists to hold vertices, faces, and texture data
all_vertices = []
all_faces = []
all_texture_coords = []
face_offset = 0

# Initialize a variable to store the texture image
texture_image = None

# Function to process each mesh and extract texture image
def process_mesh(mesh, face_offset):
    vertices = mesh.vertices  # Shape: (n_vertices, 3)
    faces = mesh.faces  # Shape: (n_faces, 3)

    # Rotate 90 degrees around x-axis
    rotation_matrix_90 = trimesh.transformations.rotation_matrix(
        np.deg2rad(90), [1, 0, 0], point=[0, 0, 0]
    )
    vertices = trimesh.transform_points(vertices, rotation_matrix_90)
    # vertices = trimesh.transform_points(vertices, rotation_matrix)

    # Adjust face indices based on the offset
    faces += face_offset

    # Extract texture coordinates if available
    if hasattr(mesh.visual, 'uv') and mesh.visual.uv is not None:
        texture_coords = mesh.visual.uv  # Shape: (n_vertices, 2)
    else:
        raise ValueError("Texture coordinates (UVs) not found in the mesh.")

    # Extract the texture image from the material
    material = mesh.visual.material
    texture_image = get_texture_image(material)

    return vertices, faces, texture_coords, texture_image

# Function to get texture image from material
def get_texture_image(material):
    if isinstance(material, trimesh.visual.material.SimpleMaterial):
        if material.image is not None:
            return material.image
    elif isinstance(material, trimesh.visual.material.PBRMaterial):
        if material.baseColorTexture is not None:
            base_color_texture = material.baseColorTexture
            # If baseColorTexture is an image
            if isinstance(base_color_texture, Image.Image):
                return base_color_texture
            # If baseColorTexture is a texture object with an image
            elif hasattr(base_color_texture, 'image') and base_color_texture.image is not None:
                return base_color_texture.image
    # Try accessing any available image in material attributes
    for attr_name in dir(material):
        attr = getattr(material, attr_name)
        if isinstance(attr, Image.Image):
            return attr
        elif hasattr(attr, 'image') and attr.image is not None:
            return attr.image
    return None

# Check if the loaded object is a Scene or a single Mesh
if isinstance(scene_or_mesh, trimesh.Scene):
    # Combine all geometries in the scene
    for geom in scene_or_mesh.geometry.values():
        vertices, faces, texture_coords, mesh_texture_image = process_mesh(geom, face_offset)

        all_vertices.append(vertices)
        all_faces.append(faces)
        all_texture_coords.append(texture_coords)

        # Use the texture image from the first mesh that has one
        if texture_image is None and mesh_texture_image is not None:
            texture_image = mesh_texture_image

        # Update the face offset
        face_offset += vertices.shape[0]
else:
    # It's a single mesh
    vertices, faces, texture_coords, texture_image = process_mesh(scene_or_mesh, face_offset)

    all_vertices.append(vertices)
    all_faces.append(faces)
    all_texture_coords.append(texture_coords)

if texture_image is None:
    raise ValueError("Texture image not found in the mesh.")

# Convert the texture image to a NumPy array
texture_array = np.array(texture_image)

# Create a PyVista Texture
texture = pv.Texture(texture_array)

# Concatenate all vertices, faces, and texture coordinates
vertices = np.vstack(all_vertices)
faces = np.vstack(all_faces)
texture_coords = np.vstack(all_texture_coords)

# Convert faces to the format expected by PyVista
n_faces = faces.shape[0]
faces_pv = np.hstack([np.full((n_faces, 1), 3), faces]).flatten()

# Create a PyVista PolyData object
polydata = pv.PolyData(vertices, faces_pv)
polydata.active_texture_coordinates = texture_coords  # Use active_texture_coordinates

# Plot the mesh with the texture applied
plotter = pv.Plotter()
plotter.add_mesh(polydata, texture=texture)
plotter.show()
