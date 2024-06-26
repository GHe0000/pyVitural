import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
from scipy.spatial import Delaunay, delaunay_plot_2d

from Vmath import *
from Vgraph import *

import yaml

testz = 0.3
editerLayer = 0
#editerLayer = -1

# 窗口初始化
#windowSize = (2048, 2048)
#windowSize = (1024, 1024)
windowSize = (512, 512)

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

# Todo
def delaunaySave(path):
    for layer in Layers:
        vertices = layer.vertices
        delaunay = layer.delaunay
        saveData = {"Vertices":vertices,"Delaunay":delaunay}
        np.savez(path + "/" + layer.name, **saveData)

# Todo
'''
def delaunayLoad(path):
    loadData = np.load(path)
    for layer in Layers:
        layer.vertices = loadData[layer.name]["Vertices"]
        layer.delaunay = loadData[layer.name]["Delaunay"]
'''

# 处理传入的命令行
def command(cmd):
    global editerLayer
    # 打印所有图层
    if cmd == "l":
        print("所有图层:")
        for i, layer in  enumerate(Layers):
            if i == editerLayer:
                print(str(i)+":"+layer.name+"(正在编辑)")
            else:
                print(str(i)+":"+layer.name)
    # Todo
    elif cmd == "save":
        if False:
            print("[CMD]没有生成Delaunay三角形")
        else:
            # 仍未写完
            #delaunaySavePath = input("输入保存路径:")
            delaunaySave("./Test/02/testDelaunay")
            #delaunaySave(delaunaySavePath)
    # 选择图层
    elif cmd == "layer":
        print("所有图层:")
        for i, layer in  enumerate(Layers):
            if i == editerLayer:
                print(str(i)+":"+layer.name+"(正在编辑)")
            else:
                print(str(i)+":"+layer.name)
        print("-1为查看所有图层")
        editerLayer = int(input("layer?:"))
    else:
        print("[CMD]未找到命令")

selectedVertex = None
def mouseCallback(window, button, action, mods):
    global selectedVertex
    global isMove
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        xpos, ypos = glfw.get_cursor_pos(window)
        width, height = windowSize
        x = (xpos / width) * 2 - 1
        y = (ypos / height) * 2 - 1
        y = -y
        # 添加节点
        if editerType == 1 and editerLayer != -1:
            pa = np.array([x,y,testz,1])
            pa = pa @ imodel
            
            px,py = pa[0], pa[1]
            a,b,c,d = Layers[editerLayer].bbox
            q, w = Layers[editerLayer].qw
            u = w*(px-a)/(c-a)
            v = q*(py-b)/(d-b)
            pb = np.array([u,v,0,1])
            vertex = np.empty(shape=(1,8))
            vertex[:,:4],vertex[:,4:] = pa, pb
            print(vertex)
            Layers[editerLayer].vertices = np.vstack((Layers[editerLayer].vertices, vertex))
            Layers[editerLayer].delaunay = np.array([])
        # 修改节点
        # 选点
        if editerType == 2 and isMove == 0 and editerLayer!= -1:
            minDistance = 0.1
            selectedVertex = None
            for i, vertices in enumerate(Layers[editerLayer].vertices):
                vertex = vertices[:4] @ model
                distance = np.linalg.norm(np.array([x, y]) - vertex[:2])
                if distance < minDistance:
                    minDistance = distance
                    selectedVertex = i
        # 移点
        if editerType == 2 and isMove == 1 and editerLayer != -1:
            if selectedVertex == None:
                print("未选点")
            else:
                pa = np.array([x,y,testz,1])
                pa = pa @ imodel
                px,py = pa[0], pa[1]
                a,b,c,d = Layers[editerLayer].bbox
                q, w = Layers[editerLayer].qw
                u = w*(px-a)/(c-a)
                v = q*(py-b)/(d-b)
                pb = np.array([u,v,0,1])
                vertex = np.empty(shape=(1,8))
                vertex[:,:4],vertex[:,4:] = pa, pb
                print(vertex)
                Layers[editerLayer].vertices[selectedVertex] = vertex
                Layers[editerLayer].delaunay = np.array([])

            isMove = 0

editerType = 1 # 当前编辑器状态
isMove = 0 # 是否正在移动
#editerLayer = -1 # 当前正在编辑的图层（-1为查看所有图层）
def keyCallback(window, key, scancode, action, mods):
    global triDelaunay
    global editerType
    global selectedVertex
    global isMove

    if key == glfw.KEY_1 and (mods & glfw.MOD_CONTROL) != 0 and action == glfw.PRESS:
        editerType = 1
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
        if editerType == 1 and editerLayer != -1:
            if np.size(Layers[editerLayer].vertices) == 0:
                print("[Ctrl-Z]列表中已经没有点，无法撤回")
            else:
                print("[Ctrl-Z]撤回列表中的最后一个点")
                Layers[editerLayer].vertices = Layers[editerLayer].vertices[:-1,:]
                Layers[editerLayer].delaunay = np.array([])
    # 计算三角划分
    if key == glfw.KEY_ENTER and action == glfw.PRESS:
        if editerType == 1 or editerType == 2:
            if Layers[editerLayer].vertices.shape[0] < 3:
                print("[Enter]点数量不够，无法计算三角划分")
            else:
                print("[Enter]开始计算三角划分")
                vertices = Layers[editerLayer].vertices
                tri = Delaunay(vertices[:,:2])
                triDelaunay = tri.simplices
                Layers[editerLayer].delaunay = triDelaunay
                print("[Enter]计算结束")
    if editerType == 2:
        # 移动点
        if key == glfw.KEY_M and action == glfw.PRESS:
            if isMove == 0:
                isMove = 1
            else:
                isMove = 0
        # 删除点
        if key == glfw.KEY_D and action == glfw.PRESS:
            if selectedVertex == None:
                print("未选点")
            else:
                Layers[editerLayer].vertices = np.delete(Layers[editerLayer].vertices, selectedVertex, axis=0)
                Layers[editerLayer].delaunay = np.array([])
                selectedVertex = None

def drawLayers():
    if editerLayer == -1:
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
    else:
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_TEXTURE_2D)
        #glBindTexture(GL_TEXTURE_2D, Layers[editerLayer].texture)
        glColor4f(1, 1, 1, 1)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        #glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        vertex = Layers[editerLayer].getVertex()
        p = vertex.reshape(4,8)
        a, b = p[:,:4], p[:,4:]
        a = a @ model
        glBegin(GL_QUADS)
        for i in range(4):
            glTexCoord4f(*b[i])
            glVertex4f(*a[i])
        glEnd()
        '''

        glDisable(GL_TEXTURE_2D)
        glColor4f(0, 0, 0, 1)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        vertex = Layers[editerLayer].getVertex()
        p = vertex.reshape(4,8)
        a, b = p[:,:4], p[:,4:]
        a = a @ model
        glBegin(GL_QUADS)
        for i in range(4):
            glTexCoord4f(*b[i])
            glVertex4f(*a[i])
        glEnd()

        '''


def drawDots():
    if editerLayer != -1:
        if np.size(Layers[editerLayer].vertices) != 0:
            Vertices = Layers[editerLayer].vertices[:,:4]
            glPointSize(5)
            glColor3f(1,0,0)
            glBegin(GL_POINTS)
            for p in Vertices:
                p = p @ model
                glVertex4f(*p)
            glEnd()
            if selectedVertex is not None and isMove == 0:
                glColor3f(0,0,1)
                glBegin(GL_POINTS)
                glVertex4f(*(Vertices[selectedVertex] @ model))
                glEnd()
            if selectedVertex is not None and isMove == 1:
                glColor3f(0,1,1)
                glBegin(GL_POINTS)
                glVertex4f(*(Vertices[selectedVertex] @ model))
                glEnd()

def drawTestDot(x,y,z):
    glPointSize(5)
    glColor3f(0,0,1)
    glBegin(GL_POINTS)
    glVertex4f(x,y,z,1)
    glEnd()

def drawDelaunay():
    if editerLayer != -1:
        if np.size(Layers[editerLayer].delaunay) != 0:
            glColor3f(1, 0, 0)
            triDelaunay = Layers[editerLayer].delaunay
            vertices = Layers[editerLayer].vertices[:,:4]
            for tri in triDelaunay:
                glBegin(GL_LINE_LOOP)
                for vertex in tri:
                    glVertex4f(*(vertices[vertex] @ model))
                glEnd()

window = initWindow()
glfw.set_mouse_button_callback(window, mouseCallback)
glfw.set_key_callback(window, keyCallback)

layerPath = "./Test/02/layer.yaml"
try:
    with open(layerPath, encoding="utf8") as f:
        layerInfo = yaml.safe_load(f)
except Exception as error:
    print(error)

Layers = []

'''
for layer in layerInfo:
    image = np.load(layerInfo[layer]["path"])
    a,b,c,d = layerInfo[layer]["bbox"]
    Layers.append(LayerInEditer(name=layer,
                                bbox=(b,a,d,c),
                                z=0.3,
                                npdata=image))
'''

# 加载图片
image = np.load("./Test/02/face.npy")
a,b,c,d = [351,241,670,560]

Layers.append(LayerInEditer(name="face",
                            bbox=(b,a,d,c),
                            z=testz,
                            npdata=image))

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
    drawLayers()
    glDisable(GL_BLEND)
    drawDelaunay()
    drawDots()
    drawTestDot(0,0,0) # 原点
    glfw.swap_buffers(window)

