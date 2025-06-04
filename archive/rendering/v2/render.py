import f3d

if __name__ == "__main__":

    f3d.Engine.autoload_plugins()  # Load static plugins
    eng = f3d.Engine(f3d.Window.NATIVE)  # Create a native window engine

    try:

        eng.loader.load_scene("models/0/mesh.glb")

    except RuntimeError as e:

        print(e)

    eng.window.render()
    eng.interactor.start()

# Anieesh Saravanan, 3, 2025