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
Layers.append(Layer(name="face",
                    vertices=,
                    delaunay=,
                    npdata=))

def drawOneLayer(layer):
    if layer.isVisual == 1:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, layer.texture)
        glColor4f(1, 1, 1, 1)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        vertex = layer.vertices.copy()
        delaunay = layer.delaunay.copy()
        ps = vertex.reshape(vertex.shape[0], 8)
        a, b = p[:,:4], p[:,4:]
        a = a @ model
        for tri in delaunay:
            glBegin(GL_TRIANGLES)
                for i in tri:
                    glTexCoord4f(*b[i])
                    glVertex4f(*a[i])
            glEnd()
