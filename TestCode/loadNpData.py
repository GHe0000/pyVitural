import numpy as np

layerData = np.load("../Test/02/testDelaunay/face.npz")
print(layerData["Vertices"])
print(layerData["Delaunay"])
