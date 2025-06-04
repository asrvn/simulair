import OpenGL.GL as gl
import glfw

glfw.init()

window = glfw.create_window(1, 1, "", None, None)

glfw.make_context_current(window)

print(gl.glGetString(gl.GL_VERSION))

glfw.terminate()

# Anieesh Saravanan, 3, 2025