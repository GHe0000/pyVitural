import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

from Vmath import *
from Vgraph import *

import yaml

windowSize = (512,512)
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

imageDate = np.load("../Test/02/face.npy")
b,a,d,c = [351,241,670,560]

psd_size = (1024,1024)
model = scale(2/psd_size[0], 2/psd_size[1], 1) @ translate(-1, -1, 0) @ rotate(-np.pi/2,axis=(0,1))
imodel = rotate(np.pi/2,axis=(0,1)) @ translate(1,1,0) @ scale(psd_size[0]/2, psd_size[1]/2, 1)

def genTexture(npdata):
    w, h = npdata.shape[:2]
    d = 2**int(max(np.log2(w), np.log2(h)) + 1)
    texture = np.zeros([d, d, 4], dtype = npdata.dtype)
    texture[:, :, :3] = 255
    texture[:w, :h] = npdata
    width, height = texture.shape[:2]
    texture_num = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_num)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_FLOAT, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glGenerateMipmap(GL_TEXTURE_2D)
    return texture_num, w/d, h/d

window = initWindow()

texture, q, w = genTexture(imageDate)
z = 0.3
'''
p1 = [a, b, z, 1, 0, 0, 0, 1]
p2 = [a, d, z, 1, w, 0, 0, 1]
p4 = [c, b, z, 1, 0, q, 0, 1]
p3 = [c, d, z, 1, w, q, 0, 1]
'''
p1 = [a, b, z, 1, 0, 0, 0, 1]
p2 = [a, d, z, 1, w, 0, 0, 1]
p4 = [c, b, z, 1, 0, q, 0, 1]
p3 = [c, d, z, 1, w, q, 0, 1]

p = np.array([[p1,p2],
              [p4,p3]])
p = p.reshape(4,8)

def drawLayers():
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glColor4f(1, 1, 1, 1)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    a, b = p[:,:4], p[:,4:]
    a = a @ model
    glBegin(GL_QUADS)
    for i in range(4):
        glTexCoord4f(*b[i])
        glVertex4f(*a[i])
    glEnd()

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClearColor(0,1,0,1) # 底部颜色
    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND)
    drawLayers()
    glDisable(GL_BLEND)
    glPointSize(5)
    glColor3f(0,0,1)
    glBegin(GL_POINTS)
    glVertex4f(*(p[:,:4]@model)[0])
    glEnd()
    glfw.swap_buffers(window)

