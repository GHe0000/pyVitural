import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
from PIL import Image

from Vmath import *
from Vgraph import *

import yaml

windowSize = (512,512)

# 新建窗口
def initWindow():
    glfw.init()
    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.RESIZABLE, False)
    window = glfw.create_window(*windowSize, "V", None, None)
    glfw.make_context_current(window)
    glViewport(0, 0, *windowSize)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glEnable(GL_MULTISAMPLE)
    glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
    return window

Layers = []

def loadOneLayerInf(path):
    loadLayerInf = np.load(path)

# Test
loadLayerInf = np.load("./Test/02/testDelaunay/face.npz")
imageNpdate = np.load("./Test/02/face.npy")

Layers.append(Layer(name="face",
                    vertices=loadLayerInf["Vertices"],
                    delaunay=loadLayerInf["Delaunay"],
                    npdata=imageNpdate))

def drawOneLayer(layer):
    if layer.isVisual == 1:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, layer.texture)
        glColor4f(1, 1, 1, 1)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        vertex = layer.vertices.copy()
        delaunay = layer.delaunay.copy()
        ps = vertex.reshape(vertex.shape[0], 8)
        a, b = ps[:,:4], ps[:,4:]
        a = a @ model
        #print(b)
        for tri in delaunay:
            glBegin(GL_TRIANGLES)
            for i in tri:
                glTexCoord4f(*b[i])
                glVertex4f(*a[i])
            glEnd()

window = initWindow()

#psd_size = (512, 512)
psd_size = (1024,1024)
model = scale(2/psd_size[0], 2/psd_size[1], 1) @ translate(-1, -1, 0) @ rotate(-np.pi/2,axis=(0,1))
imodel = rotate(np.pi/2,axis=(0,1)) @ translate(1,1,0) @ scale(psd_size[0]/2, psd_size[1]/2, 1)

# 绘图循环
while not glfw.window_should_close(window):
    glfw.poll_events()
    glClearColor(0,0,0,0) # 底部颜色
    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND)
    drawOneLayer(Layers[0])
    #drawTestDot(0,0,0) # 原点
    glfw.swap_buffers(window)

