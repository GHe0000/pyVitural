import numpy as np
import psd_tools
import yaml

psdPath = './02/test2.psd'
psd = psd_tools.PSDImage.open(psdPath)

psdDict = {}

for layer in psd:
    print(layer.name)
    print(np.array(layer.bbox))
    a, b, c, d = layer.bbox
    savePath = "./02/" + layer.name + ".npy"
    npdata = layer.numpy()
    np.save(savePath, npdata)
    filePath = "./Test/02/" + layer.name + ".npy"
    psdDict[layer.name] = {"path":filePath,"bbox":[a,b,c,d]}

with open("./02/layer.yaml", 'w', encoding='utf-8') as f:
    yaml.dump(psdDict, f, allow_unicode=True)


