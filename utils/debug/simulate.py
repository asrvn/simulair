import trimesh
import pyvista as pv
import numpy as np
from PIL import Image

def load_mesh_and_texture(file_path):

    try:

        mesh = trimesh.load(file_path)

        pv_mesh = None
        textures = []

        if isinstance(mesh, trimesh.Trimesh):

            faces = np.hstack([np.full((len(mesh.faces), 1), 3), mesh.faces]).astype(np.int32)
            pv_mesh = pv.PolyData(mesh.vertices, faces)

            if isinstance(mesh.visual.material, trimesh.visual.material.PBRMaterial):

                base_color_texture = getattr(mesh.visual.material, 'baseColorTexture', None)

                if base_color_texture is not None:

                    texture_image = np.array(base_color_texture)
                    textures.append(texture_image)

        elif isinstance(mesh, trimesh.Scene):

            combined_mesh = pv.MultiBlock()

            for name, geom in mesh.geometry.items():

                faces = np.hstack([np.full((len(geom.faces), 1), 3), geom.faces]).astype(np.int32)
                pv_submesh = pv.PolyData(geom.vertices, faces)
                combined_mesh.append(pv_submesh)

                if isinstance(geom.visual.material, trimesh.visual.material.PBRMaterial):

                    base_color_texture = getattr(geom.visual.material, 'baseColorTexture', None)

                    if base_color_texture is not None:

                        texture_image = np.array(base_color_texture)
                        textures.append(texture_image)

            pv_mesh = combined_mesh

        else:

            raise TypeError(f"Unsupported mesh type: {type(mesh)}")

        return pv_mesh, textures

    except Exception as e:

        print(f"Failed to load mesh or texture from {file_path}: {e}")
        return None, []

def apply_texture(pv_mesh, texture_image):

    if texture_image is not None and isinstance(pv_mesh, pv.PolyData):

        try:

            if texture_image.ndim == 3:  # Ensure it's an image

                pv_texture = pv.numpy_to_texture(texture_image)
                pv_mesh.texture_map_to_plane(inplace=True)
                return pv_mesh, pv_texture

        except Exception as e:

            print(f"Failed to apply texture: {e}")

    return pv_mesh, None

def render_scene(file_paths):

    plotter = pv.Plotter()
    positions = [(0, 0, 0), (1.5, 0, 0), (-1.5, 0, 0)]

    for i, file_path in enumerate(file_paths):

        pv_mesh, textures = load_mesh_and_texture(file_path)

        if pv_mesh is not None:

            if isinstance(pv_mesh, pv.MultiBlock):

                for j in range(pv_mesh.GetNumberOfBlocks()) :

                    submesh = pv_mesh.GetBlock(j)

                    if submesh is not None:

                        texture_image = textures[j] if j < len(textures) else None
                        submesh, pv_texture = apply_texture(submesh, texture_image)
                        # Apply direct vertex manipulation for translation
                        submesh.points += np.array(positions[i]) + np.array([j * 5, 0, 0])  # Larger separation for submeshes
                        plotter.add_mesh(submesh, texture=pv_texture, show_edges=False)

            else:

                texture_image = textures[0] if textures else None
                pv_mesh, pv_texture = apply_texture(pv_mesh, texture_image)
                # Directly manipulate the vertices to translate the mesh
                pv_mesh.points += np.array(positions[i])
                plotter.add_mesh(pv_mesh, texture=pv_texture, show_edges=False)

    plotter.show_axes()
    plotter.show()

if __name__ == "__main__":

    glb_file_paths = [
        'models/0/mesh.glb',
        'models/1/mesh.glb',
        'models/2/mesh.glb'
    ]

    render_scene(glb_file_paths)