import numpy as np

# 这是一个数学计算库，用于计算各种常用的变换的矩阵

# （相对原点）缩放
def scale(x, y, z):
    a = np.eye(4, dtype=np.float32)
    a[0, 0] = x
    a[1, 1] = y
    a[2, 2] = z
    return a

# （相对原点）旋转
def rotate(r, axis: tuple):
    a = np.eye(4, dtype = np.float32)
    a[axis[0], axis[0]] = np.cos(r)
    a[axis[0], axis[1]] = np.sin(r)
    a[axis[1], axis[0]] = - np.sin(r)
    a[axis[1], axis[1]] = np.cos(r)
    return a

# 平移
def translate(x, y, z):
    a = np.eye(4, dtype = np.float32)
    a[3, 0] = x
    a[3, 1] = y
    a[3, 2] = z
    return a

# 透视缩放
def perspective():
    a = np.eye(4, dtype = np.float32)
    a[2, 2] = 1 / 1000
    a[3, 2] = -0.0001
    a[2, 3] = 1
    a[3, 3] = 0
    return a

# 透视缩放的逆运算
def inperspective():
    a = np.eye(4, dtype = np.float32)
    a[2, 2] = 0
    a[3, 2] = 1
    a[2, 3] = -10000
    a[3, 3] = 10
    return a

# 指定点的旋转
def tran_and_rot(dx, dy, rot):
    view = perspective() @ translate(-dx, -dy, 0) @ inperspective()
    view = view @ translate(0, 0, -0.3)
    view = view @ rotate(rot[0], axis=(0, 2)) @ rotate(rot[1], axis=(2, 1)) @ rotate(rot[2], axis=(0, 1))
    view = view @ translate(0,0,0.3)
    view = view @ perspective() @ translate(dx, dy, 0) @ inperspective()
    return view


