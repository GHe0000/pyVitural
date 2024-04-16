import time
import logging

import numpy as np

import socket, struct

import get_feature_by_openseeface
import threading

address = ("127.0.0.1", 4242)
buf = bytearray(8 * 6)
data = [1, 2, 3, 4, 5, 6]

feature = np.zeros(11)

def opentrack_post():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while True:
            get_feature = get_feature_by_openseeface.get_feature()
            data = [get_feature[0] * 5,
                    get_feature[1] * 5,
                    get_feature[5],
                    np.arcsin(get_feature[2])/np.pi * 180,
                    - np.arcsin(get_feature[3])/np.pi * 180,
                    np.arcsin(get_feature[4])/np.pi * 180]
            struct.pack_into('dddddd', buf, 0, *data)
            sock.sendto(buf, address)

t = threading.Thread(target = opentrack_post)
t.setDaemon(True)
t.start()
logging.warning("OpenTrack Post Starting......")

np.set_printoptions(suppress=True)
np.set_printoptions(linewidth=400)
if __name__ == "__main__":
    while True:
        time.sleep(0.1)
        # x, y, yaw, pitch, roll, face, eye_l, eye_r, brow_l, brow_r, mouth
        print(data)