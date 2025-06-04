import trimesh
import pyvista as pv
import numpy as np
from PIL import Image

separation = 1.0

# List of GLB file paths to render
glb_files = [
    '../../models/aniketh/mesh.glb',
    '../../models/arjun/mesh.glb',
    # Add more file paths as needed
]

# Initialize the PyVista plotter
plotter = pv.Plotter()

# Function to process each mesh and extract texture image
def process_mesh(mesh):
    vertices = mesh.vertices  # Shape: (n_vertices, 3)
    faces = mesh.faces  # Shape: (n_faces, 3)

    # Rotate the vertices to make x-z plane the base
    rotation_matrix = trimesh.transformations.rotation_matrix(
        np.deg2rad(90), [1, 0, 0], point=[0, 0, 0]
    )
    vertices = trimesh.transform_points(vertices, rotation_matrix)

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

# Process each GLB file
for index, file_path in enumerate(glb_files):
    # Load the GLB file
    scene_or_mesh = trimesh.load(file_path)

    # Check if the loaded object is a Scene or a single Mesh
    meshes = []
    if isinstance(scene_or_mesh, trimesh.Scene):
        # Collect all geometries in the scene
        for geom in scene_or_mesh.geometry.values():
            meshes.append(geom)
    else:
        # It's a single mesh
        meshes.append(scene_or_mesh)

    # Process each mesh in the GLB file
    for mesh in meshes:
        vertices, faces, texture_coords, texture_image = process_mesh(mesh)

        # Apply a translation to position the object apart
        translation_vector = np.array([index * separation, 0, 0])
        vertices += translation_vector

        # Convert faces to the format expected by PyVista
        n_faces = faces.shape[0]
        faces_pv = np.hstack([np.full((n_faces, 1), 3), faces]).flatten()

        # Create a PyVista PolyData object
        polydata = pv.PolyData(vertices, faces_pv)
        polydata.active_texture_coordinates = texture_coords

        if texture_image is None:
            raise ValueError(f"Texture image not found in the mesh from file: {file_path}")

        # Convert the texture image to a NumPy array
        texture_array = np.array(texture_image)

        # Create a PyVista Texture
        texture = pv.Texture(texture_array)

        # Add the mesh to the plotter with the texture
        # plotter.add_mesh(polydata, texture=texture)
        plotter.add_mesh(polydata, texture= texture, diffuse=0.5, ambient=0.5)
        # mess around with emissive

        plotter.add_axes()

# Show the combined scene
plotter.show()
