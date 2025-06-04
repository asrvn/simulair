import f3d

if __name__ == "__main__":

    # Load static plugins
    f3d.Engine.autoload_plugins()

    # Create a native window engine
    eng = f3d.Engine(f3d.Window.NATIVE)

    # Load a model
    try:

        eng.loader.load_scene("../../models/0/mesh.glb")

    except RuntimeError as e:

        print(e)

    # Render
    eng.window.render()

    # Start interaction
    eng.interactor.start()