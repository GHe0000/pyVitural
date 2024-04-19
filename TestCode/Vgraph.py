import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

# 这是一个用来进行渲染的图形库

# 编辑器导入时使用的 Layer 类
class LayerInEditer:
    def __init__(self, name, bbox, z, npdata):
        self.name = name
        self.bbox = bbox
        self.z = z
        self.npdata = npdata
        self.texture, q, w = self.genTexture()
        self.qw = (q,w)
        self.vertices = np.empty(shape=(0,8))
        self.delaunay = np.empty(shape=(0,3))

        a,b,c,d = bbox
        # p1 p2
        # p4 p3
        p1 = [a, b, z, 1, 0, 0, 0, 1]
        p2 = [a, d, z, 1, w, 0, 0, 1]
        p4 = [c, b, z, 1, 0, q, 0, 1]
        p3 = [c, d, z, 1, w, q, 0, 1]

        self.vertex = np.array([[p1,p2],
                                [p3,p4]])

    def genTexture(self):
        w, h = self.npdata.shape[:2]
        d = 2**int(max(np.log2(w), np.log2(h)) + 1)
        texture = np.zeros([d, d, 4], dtype = self.npdata.dtype)
        texture[:, :, :3] = 255
        texture[:w, :h] = self.npdata

        width, height = texture.shape[:2]
        texture_num = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_num)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_FLOAT, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)

        return texture_num, w/d, h/d

    def getVertex(self):
        return self.vertex.copy()

# 正式使用的 Layer 类（使用 Delaunay 三角划分）
class Layer:
    def __init__(self, name, vertices, delaunay ,npdata):
        self.name = name # 名字
        # 顶点位置参数
        # 应该传入一个 Numpy 数组，每一行为一个节点
        # 前4个参数为顶点的四维齐次座标(x,y,z,w)(使用PSD座标系)
        # 后4个参数为Texture的四维齐次座标(w,q,0,1)
        # Texture齐次座标中w,q为(0,1)
        self.vertices = vertices
        # 原始的顶点位置参数，同上，但不会修改
        self.originalVertices = vertices
        self.delaunay = delaunay # Delaunay 三角分割（应该是一个 Numpy 数组）
        self.npdata = npdata # 图层 npdata 数据
        self.isVisual = 1 # 是否可见
        self.texture, q, w = self.genTexture() # 纹理编号

    def genTexture(self):
        w, h = self.npdata.shape[:2]
        d = 2**int(max(np.log2(w), np.log2(h)) + 1)
        texture = np.zeros([d, d, 4], dtype = self.npdata.dtype)
        texture[:, :, :3] = 255
        texture[:w, :h] = self.npdata

        width, height = texture.shape[:2]
        texture_num = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_num)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_FLOAT, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)

        return texture_num, w/d, h/d
