import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
from scipy.spatial import Delaunay

from Vmath import *
from Vgraph import *

# 窗口初始化
def initWindow(v_size=(512,512)):
    glfw.init()
    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.RESIZABLE, False)
    window = glfw.create_window(*v_size, "V", None, None)
    glfw.make_context_current(window)
    glViewport(0, 0, *v_size)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glEnable(GL_MULTISAMPLE)
    glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
    return window

window = initWindow()

def mouseCallback(window, button, action, mods):
    global Vertices
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        x, y = glfw.get_cursor_pos(window)
        print("Add:"+str(x)+"/"+str(y))
        Vertices.append((x, y))

glfw.make_context_current(window)
glfw.set_mouse_button_callback(window, mouseCallback)

# 加载图片
image = np.load("./Test/face.npy")
a,b,c,d = [351,241,670,560]
bbox = (b,a,d,c)

Layers = []
Layers.append(LayerInEditer(name="face",
                           bbox=bbox,
                           z=0.3,
                           npdata=image))

psd_size = (1024,1024)
model = scale(2/psd_size[0],2/psd_size[1],1) @ translate(-1,-1,0) @ rotate(-np.pi/2,axis=(0,1))

def drawLayers():
    for layer in Layers:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, layer.texture)
        glColor4f(1, 1, 1, 1)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        vertex = layer.getVertex()
        p = vertex.reshape(4,8)
        a, b = p[:,:4], p[:,4:]
        a = a @ model
        glBegin(GL_QUADS)
        for i in range(4):
            glTexCoord4f(*b[i])
            glVertex4f(*a[i])
        glEnd()

Vertices = []
def drawDots():
    if Vertices != []:
        glPointSize(5)
        glColor3f(1.0,0.0,0.0)
        glBegin(GL_POINTS)
        for p in Vertices:
            glVertex4f(*p)
        glEnd()

def drawDelaunay():
    return 0

# 绘图循环
while not glfw.window_should_close(window):
    glfw.poll_events()
    glClearColor(0,0,0,0)
    glClear(GL_COLOR_BUFFER_BIT)
    drawLayers()
    glfw.swap_buffers(window)




"""

# 顶点数据
vertices = []
def mouse_button_callback(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        x, y = glfw.get_cursor_pos(window)
        print("Add:"+str(x)+"/"+str(y))
        vertices.append((x, y))
glfw.set_mouse_button_callback(window, mouse_button_callback)

while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # 绘制图片
    glBegin(GL_QUADS)
    glEnd()

    # 绘制顶点
    glColor3f(1, 1, 1)
    glBegin(GL_POINTS)
    for vertex in vertices:
        glVertex2f(*vertex)
    glEnd()

    # 检查是否按下回车键
    if glfw.get_key(window, glfw.KEY_ENTER) == glfw.PRESS:
        if len(vertices) >= 3:
            tri = Delaunay(np.array(vertices))
            glColor3f(1, 0, 0)
            glBegin(GL_TRIANGLES)
            for simplex in tri.simplices:
                for vertex in simplex:
                    glVertex2f(*vertices[vertex])
            glEnd()
    glfw.swap_buffers(window)
glfw.terminate()
"""
