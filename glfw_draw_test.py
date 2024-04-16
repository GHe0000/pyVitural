import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

def draw_triangle(vertices):
    glBegin(GL_TRIANGLES)
    for vertex in vertices:
        glVertex3fv(vertex)
    glEnd()

def main():
    if not glfw.init():
        sys.exit()

    window = glfw.create_window(800, 600, "Draggable Triangle", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)
    glfw.set_cursor_pos_callback(window, mouse_callback)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    global vertices
    vertices = [
        [-0.5, -0.5, 0.0],
        [0.5, -0.5, 0.0],
        [0.0, 0.5, 0.0]
    ]

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        draw_triangle(vertices)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

def mouse_callback(window, xpos, ypos):
    global vertices
    width, height = glfw.get_framebuffer_size(window)
    x = (xpos / width) * 2 - 1
    y = (ypos / height) * 2 - 1
    y = -y
    print(vertices)
    print(str(x)+"/"+str(y))
    selected_vertex = None
    min_distance = 0.1

    for i, vertex in enumerate(vertices):
        distance = np.linalg.norm(np.array([x, y]) - np.array(vertex[:2]))
        if distance < min_distance:
            min_distance = distance
            selected_vertex = i

    if selected_vertex is not None:
        vertices[selected_vertex][0] = x
        vertices[selected_vertex][1] = y

if __name__ == "__main__":
    main()
