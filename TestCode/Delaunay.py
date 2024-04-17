import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt

# 定义点集
points = np.array([[0, 0], [1, 0], [0, 1], [1, 1], [0.5, 0.5]])

# 创建Delaunay对象
tri = Delaunay(points)

# 可视化结果
plt.triplot(points[:, 0], points[:, 1], tri.simplices)
plt.plot(points[:, 0], points[:, 1], 'o')
plt.show()
