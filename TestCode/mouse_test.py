import glfw
from OpenGL.GL import *

def mouse_button_callback(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        x, y = glfw.get_cursor_pos(window)
        print("鼠标左键点击位置：", x, y)

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Mouse Click Position", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

