import f3d
import numpy as np
import cv2
import trimesh
from PIL import Image

if __name__ == "__main__":

    # Generate an ArUco marker using modern OpenCV functions
    marker_id = 0
    marker_size = 512

    # Use getPredefinedDictionary and generateImageMarker
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)

    # Invert colors to have a white background with black marker patterns
    marker_image = cv2.bitwise_not(marker_image)

    # Create a larger white image to serve as the texture
    texture_size = 1024  # Larger size for the texture
    texture_image = np.ones((texture_size, texture_size), dtype=np.uint8) * 255  # White background

    # Calculate the position to place the marker image in the center
    start_point = ((texture_size - marker_size) // 2, (texture_size - marker_size) // 2)

    # Place the marker image onto the white background
    texture_image[
        start_point[1]:start_point[1] + marker_size,
        start_point[0]:start_point[0] + marker_size
    ] = marker_image

    # Create a rectangular prism mesh with a small height
    def create_box_mesh(size=1.0, height=0.1):
        """
        Creates a rectangular prism (box) mesh centered at the origin.

        Parameters:
            size (float): The length of one side of the square base.
            height (float): The height of the box.

        Returns:
            mesh (trimesh.Trimesh): The created box mesh.
        """
        # Define half dimensions
        half_size = size / 2.0
        half_height = height / 2.0

        # Define vertices
        vertices = np.array([
            # Bottom face (z = -half_height)
            [-half_size, -half_size, -half_height],  # Vertex 0
            [ half_size, -half_size, -half_height],  # Vertex 1
            [ half_size,  half_size, -half_height],  # Vertex 2
            [-half_size,  half_size, -half_height],  # Vertex 3
            # Top face (z = half_height)
            [-half_size, -half_size,  half_height],  # Vertex 4
            [ half_size, -half_size,  half_height],  # Vertex 5
            [ half_size,  half_size,  half_height],  # Vertex 6
            [-half_size,  half_size,  half_height],  # Vertex 7
        ])

        # Define faces (two triangles per face)
        faces = np.array([
            # Bottom face (normals pointing down)
            [0, 2, 1],
            [0, 3, 2],
            # Top face (normals pointing up)
            [4, 5, 6],
            [4, 6, 7],
            # Front face
            [1, 2, 6],
            [1, 6, 5],
            # Back face
            [0, 7, 3],
            [0, 4, 7],
            # Left face
            [0, 1, 5],
            [0, 5, 4],
            # Right face
            [2, 3, 7],
            [2, 7, 6],
        ])

        # Define texture coordinates (UVs)
        uvs = np.zeros((8, 2))

        # Calculate UV coordinates for the marker
        start_u = start_point[0] / texture_size
        start_v = start_point[1] / texture_size
        end_u = (start_point[0] + marker_size) / texture_size
        end_v = (start_point[1] + marker_size) / texture_size

        # Assign UVs to the top face vertices for the marker texture
        uvs[4] = [start_u, start_v]  # Vertex 4 (bottom-left of top face)
        uvs[5] = [end_u, start_v]    # Vertex 5 (bottom-right of top face)
        uvs[6] = [end_u, end_v]      # Vertex 6 (top-right of top face)
        uvs[7] = [start_u, end_v]    # Vertex 7 (top-left of top face)

        # Map the sides to a small white area in the texture to avoid black fragments
        side_u_start = 0.0
        side_v_start = 0.0
        side_u_end = start_u - 0.01  # Slightly before the marker starts
        side_v_end = 1.0

        # Assign UVs for the sides and bottom face
        # Bottom face
        uvs[0] = [side_u_start, side_v_start]
        uvs[1] = [side_u_end, side_v_start]
        uvs[2] = [side_u_end, side_v_end]
        uvs[3] = [side_u_start, side_v_end]

        # Front face (Vertices 1, 2, 6, 5)
        # Left face (Vertices 0, 1, 5, 4)
        # Right face (Vertices 2, 3, 7, 6)
        # Back face (Vertices 0, 3, 7, 4)
        # Since the vertices are shared, the UVs are already assigned for these vertices

        # Create the mesh
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

        # Assign texture coordinates
        mesh.visual = trimesh.visual.TextureVisuals(uv=uvs)

        return mesh

    # Create the box mesh
    box_mesh = create_box_mesh(size=1.0, height=0.1)

    # Apply the marker as a texture
    def apply_texture(mesh, image):
        """
        Applies a texture image to a mesh.

        Parameters:
            mesh (trimesh.Trimesh): The mesh to apply the texture to.
            image (numpy.ndarray): The texture image.

        Returns:
            mesh (trimesh.Trimesh): The textured mesh.
        """
        # Convert the image to RGB if it's grayscale
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        # Convert the image to a PIL image
        texture_image = Image.fromarray(image)
        # Create a SimpleMaterial with the image
        material = trimesh.visual.material.SimpleMaterial(
            image=texture_image,
            diffuse=[1.0, 1.0, 1.0],   # Set diffuse color to white
            specular=[1.0, 1.0, 1.0],  # Set specular color to white
            ambient=[1.0, 1.0, 1.0],   # Set ambient color to white
        )
        # Assign the material to the mesh's visual
        mesh.visual.material = material
        return mesh

    # Apply the marker as a texture
    textured_mesh = apply_texture(box_mesh, texture_image)

    # Export the mesh to a GLB file
    glb_filename = "../../models/aruco/mesh.glb"
    glb_data = trimesh.exchange.gltf.export_glb(textured_mesh)
    with open(glb_filename, 'wb') as f:
        f.write(glb_data)
    print(f"GLB file saved as '{glb_filename}'")

    # Load static plugins
    f3d.Engine.autoload_plugins()

    # Create a native window engine
    eng = f3d.Engine(f3d.Window.NATIVE)

    # Load the model
    try:
        eng.loader.load_scene(glb_filename)
    except RuntimeError as e:
        print(e)

    # Adjust renderer options


    # Render
    eng.window.render()

    # Start interaction
    eng.interactor.start()
