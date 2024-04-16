import time
import logging
import threading
import numpy as np

import socket
import struct

target_ip = "127.0.0.1"
target_port = 11573

class SlidingAverage:
    def __init__(self, num, l):
        self.S = np.zeros((l, num))

    def update(self, new):
        self.S = np.delete(self.S,0,axis=0)
        self.S = np.vstack((self.S,new))
        return np.average(self.S,axis=0)

class SlidingAverageXY:
    def __init__(self, l):
        self.l = l
        self.S = [np.zeros((self.l, 2))] * 68

    def update(self, new):
        rtn = [np.zeros((self.l, 2))] * 68
        for i in range(68):
            self.S[i] = np.delete(self.S[i],0,axis=0)
            self.S[i] = np.vstack((self.S[i],new[i]))
            rtn[i] = np.average(self.S[i],axis=0)
        return rtn

class KalmanFilterSimple:
    def __init__(self):
        self.K = 0
        self.X = 0
        self.P = 0.1
        self.Q = 0.008
        self.R = 0.0005

    def update(self, z):
        self.K = self.P / (self.P + self.R)
        self.X = self.X + self.K * (z - self.X)
        self.P = self.P - self.K * self.P + self.Q
        return self.X

class KalmanFilter:
    def __init__(self, m, Qval, Rval):
        self.K = np.zeros((m,m))
        self.X = np.zeros(m)
        self.P = np.eye(m)
        self.F = np.eye(m)
        self.B = np.eye(m)
        self.H = np.eye(m)
        self.Q = Qval * np.eye(m)
        self.R = Rval * np.eye(m)

    def update(self, uu, zz):
        self.X = self.F @ self.X + self.B @ uu
        self.P = self.F @ self.P @ self.F.T + self.Q
        self.K = self.P @ self.H.T @ np.linalg.inv(self.H @ self.P @ self.H.T + self.R)
        self.X = self.X + self.K @ (zz - self.H @ self.X)
        self.P = self.P - self.K @ self.H @ self.P
        return self.X

class DynamicsControl:
    def __init__(self, M=1, ALPHA=0.7, KP=0.04, KD=1):
        self.T = 0.1 # time interval
        self.ALPHA = ALPHA # incomplete derivative coefficient
        self.KP = KP
        self.KD = KD
        self.M = M # mass
        self.a = 0 # acceleration
        self.v = 0 # velocity
        self.x = 0 # position
        self.x_d = 0 # desired position
        self.e = 0 # error
        self.e_1 = 0 # last error
        self.de = 0 # derivative of error
        self.p_out = 0 # proportional termd_outd_out_1
        self.d_out = 0 # derivative term
        self.d_out_1 = 0 #  last derivative term 
        self.F = 0 # control force

        self.THRESH = 0.05 # control law changing threshold
    
    def update(self, X):
        self.x_d = self.x
        self.x = X

        self.e = self.x_d - self.x # Update error
        self.de = (self.e - self.e_1)/self.T # Compute the derivative of error
        self.p_out = self.KP*self.e
        self.d_out = (1-self.ALPHA)*self.KD*self.de + self.ALPHA*self.d_out_1

        self.F = self.p_out + self.d_out # Update control force

        self.e_1 = self.e # Update last error
        self.d_out_1 = self.d_out # Update last derivative term

        self.a = self.F/self.M # Update acceleration
        self.v = self.v + self.a*self.T # Update velocity
        self.x = self.x + self.v*self.T # Update position
        if self.x < 0:
            self.x = np.array([0.03])
        return self.x

def loop_func():
    global feature
    feature = np.array([0,0,0,0,0,0,0,0,0,0,0])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((target_ip, target_port))

    logging.warning("server start at: %s:%s" % (target_ip, target_port))
    logging.warning("wait for connection......")

    SlidingAverage1 = SlidingAverage(2,5)
    SlidingAverage2 = SlidingAverage(3,5)
    SlidingAverage3 = SlidingAverage(2,5)
    SlidingAverage4 = SlidingAverage(2,3)

    while True:
        indata, addr = sock.recvfrom(2048)
        A = struct.unpack("=di4fB11f",indata[:73])
        B = struct.unpack("14f",indata[-56:])

        rlt_pos = np.array([A[16], A[15]])
        face = np.array([A[17]])

        rot = np.array([
                np.sin(np.pi * A[13]/180),
                np.sin(np.pi * ((A[12]-180)/180)),
                np.sin(np.pi * (A[14]-90)/180)
              ])
        
        eye = np.array([A[5], A[4]])
        brow = np.array([B[2], B[5]])
        mouth = np.array([B[12]])

        rlt_pos = SlidingAverage1.update(rlt_pos)
        rot = SlidingAverage2.update(rot)
        brow = SlidingAverage3.update(brow)
        eye = SlidingAverage4.update(eye)
        feature = np.concatenate([rlt_pos, rot, face, eye, brow, mouth])
    sock.close()

def get_feature():
    return feature

t = threading.Thread(target = loop_func)
t.setDaemon(True)
t.start()
logging.warning("FaceTracter Starting......")

np.set_printoptions(suppress=True)
np.set_printoptions(linewidth=400)
if __name__ == "__main__":
    while True:
        time.sleep(0.1)
        # x, y, yaw, pitch, roll, face, eye_l, eye_r, brow_l, brow_r, mouth
        print(feature)
