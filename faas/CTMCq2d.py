import numpy as np 
import math

def poisson(r, t, n):
    return ((r * t)**n)*np.exp(-r*t) / math.factorial(n)

data = np.loadtxt("../trace-final.csv", skiprows=1, delimiter=',', dtype=int)
time = 30 * 24 * 60 * 60 # in ms
np.set_printoptions(suppress=True)

s1, r1 = 1 / data[0, 1], data[0, 2] / time
s2, r2 = 1 / data[1, 1], data[1, 2] / time
a = 0.5

genMatrix = np.array([[-s1, s1      ,  0, 0  , 0       , 0 , 1],
                      [r1 , -(r1+r2), 0 , 0  , 0       , r2, 1],
                      [a  , 0       , -a, 0  , 0       , 0 , 1],
                      [0  , 0       , 0 , -s2, s2      , 0 , 1],
                      [0  , 0       , r1, r2 , -(r1+r2), 0 , 1],
                      [0  , 0       , 0 , a  , 0       , -a, 1]], dtype=float)

b = np.array([[0], [0], [0], [0], [0], [0], [1]])
genMatrixT = np.transpose(genMatrix)
p = np.linalg.lstsq(np.transpose(genMatrix), b, rcond=None)[0]

ar1, ar2 = 1/r1, 1/r2


print(p)
print("CS ratio  = ", (ar2 / (ar2 + ar1)) * p[1] + (ar1 / (ar2 + ar1)) * p[4])
print("Loss rate = ", p[0] + p[2] + p[3] + p[5])
