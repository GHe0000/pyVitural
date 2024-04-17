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
    #glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)
    glViewport(0, 0, *v_size)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glEnable(GL_MULTISAMPLE)
    glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
    return window

def command(cmd):
    if cmd == "l":
        print("所有图层:")
        for layer in Layers:
            print(layer.name)
    else:
        print("[CMD]未找到命令")

selectedVertex = None
def mouseCallback(window, button, action, mods):
    global Vertices
    global selectedVertex
    global isMove
    global haveDelaunay
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        xpos, ypos = glfw.get_cursor_pos(window)
        width, height = glfw.get_framebuffer_size(window)
        x = (xpos / width) * 2 - 1
        y = (ypos / height) * 2 - 1
        y = -y
        if editerType == 1:
            print("Add:"+str(x)+"/"+str(y))
            Vertices.append((x, y))
            haveDelaunay = 0
        if editerType == 2 and isMove == 0:
            minDistance = 0.1
            selectedVertex = None
            for i, vertex in enumerate(Vertices):
                distance = np.linalg.norm(np.array([x, y]) - np.array(vertex[:2]))
                if distance < minDistance:
                    minDistance = distance
                    selectedVertex = i
        if editerType == 2 and isMove == 1:
            if selectedVertex == None:
                print("未选点")
            else:
                Vertices[selectedVertex] = [x,y]
                haveDelaunay = 0
            isMove = 0

editerType = 1
isMove = 0
def keyCallback(window, key, scancode, action, mods):
    global Vertices
    global triDelaunay
    global haveDelaunay
    global editerType
    global selectedVertex
    global isMove

    if key == glfw.KEY_1 and (mods & glfw.MOD_CONTROL) != 0 and action == glfw.PRESS:
        editerType = 1
        haveDelaunay = 0
        selectedVertex = None
        print("[Mode]添加节点模式")
    if key == glfw.KEY_2 and (mods & glfw.MOD_CONTROL) != 0 and action == glfw.PRESS:
        editerType = 2
        print("[Mode]编辑节点模式")
    if key == glfw.KEY_0 and (mods & glfw.MOD_CONTROL) != 0 and action == glfw.PRESS:
        editerType = 0
        print("[Mode]命令行输入")
        cmd = input("?:")
        command(cmd)
        editerType = 1
        print("[Mode]添加节点模式")
    # Ctrl-Z
    if key == glfw.KEY_Z and (mods & glfw.MOD_CONTROL) != 0 and action == glfw.PRESS:
        if editerType == 1:
            if Vertices == []:
                print("[Ctrl-Z]列表中已经没有点，无法撤回")
            else:
                print("[Ctrl-Z]撤回列表中的最后一个点")
                Vertices.pop()
                haveDelaunay = 0
    # Enter
    if key == glfw.KEY_ENTER and action == glfw.PRESS:
        if editerType == 1 or editerType == 2:
            if len(Vertices) < 3:
                print("[Enter]点数量不够，无法计算三角划分")
            else:
                print("[Enter]开始计算三角划分")
                tri = Delaunay(np.array(Vertices))
                triDelaunay = tri.simplices
                haveDelaunay = 1
                print("[Enter]计算结束")
                #print(triDelaunay.type)
    if editerType == 2:
        if key == glfw.KEY_M and action == glfw.PRESS:
            if isMove == 0:
                isMove = 1
            else:
                isMove = 0
        if key == glfw.KEY_D and action == glfw.PRESS:
            if selectedVertex == None:
                print("未选点")
            else:
                Vertices.pop(selectedVertex)
                haveDelaunay = 0
                selectedVertex = None

def drawLayers():
    for layer in Layers:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, layer.texture)
        glColor4f(1, 1, 1, 1)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        vertex = layer.getVertex()
        p = vertex.reshape(4,8)
        a, b = p[:,:4], p[:,4:]
        a = a @ model # Mark
        glBegin(GL_QUADS)
        for i in range(4):
            glTexCoord4f(*b[i])
            glVertex4f(*a[i])
        glEnd()

Vertices = []
def drawDots():
    if Vertices != []:
        glPointSize(5)
        glColor3f(1,0,0)
        glBegin(GL_POINTS)
        for p in Vertices:
            glVertex2f(*p)
        glEnd()
        if selectedVertex is not None and isMove == 0:
            glColor3f(0,0,1)
            glBegin(GL_POINTS)
            glVertex2f(*Vertices[selectedVertex])
            glEnd()
        if selectedVertex is not None and isMove == 1:
            glColor3f(0,1,1)
            glBegin(GL_POINTS)
            glVertex2f(*Vertices[selectedVertex])
            glEnd()

def drawTestDot(x,y,z):
    glPointSize(5)
    glColor3f(0,0,1)
    glBegin(GL_POINTS)
    glVertex4f(x,y,z,1)
    glEnd()

haveDelaunay = 0
def drawDelaunay():
    if haveDelaunay != 0:
        glColor3f(1, 0, 0)
        for tri in triDelaunay:
            glBegin(GL_LINE_LOOP)
            for vertex in tri:
                glVertex2f(*Vertices[vertex])
            glEnd()

window = initWindow()
glfw.set_mouse_button_callback(window, mouseCallback)
glfw.set_key_callback(window, keyCallback)

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
# 绘图循环

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClearColor(0,0,0,0) # 底部颜色
    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND)
    drawLayers()
    glDisable(GL_BLEND)
    drawDelaunay()
    drawDots()
    drawTestDot(0,0,0) # 原点
    glfw.swap_buffers(window)

