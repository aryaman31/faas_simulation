import numpy as np 
import math

def poisson(r, t, n):
    return ((r * t)**n)*np.exp(-r*t) / math.factorial(n)

data = np.loadtxt("../trace-final.csv", skiprows=1, delimiter=',', dtype=int)
time = 30 * 24 * 60 * 60 # in ms
np.set_printoptions(suppress=True)

s1, r1 = 1000 / data[0, 1], data[0, 2] / time
s2, r2 = 1000 / data[1, 1], data[1, 2] / time
a = 0.5

genMatrix = np.array([[-s1, s1      ,  0, 0  , 0       , 1 ],
                      [r1 , -(r1+r2), 0 , 0  , 0       , 1 ],
                      [a  , 0       , -a, 0  , 0       , 1 ],
                      [0  , 0       , 0 , -s2, s2      , 1 ],
                      [0  , 0       , r1, r2 , -(r1+r2), 1 ],
                      [0  , 0       , 0 , a  , 0       , 1]], dtype=float)

b = np.array([[0], [0], [0], [0], [0], [1]])
genMatrixT = np.transpose(genMatrix)
# p = np.linalg.lstsq(np.transpose(genMatrix), b, rcond=None)[0]
p = b.T @ np.linalg.inv(genMatrix)
print(p)
p = p[0]

print(p)
print("CS ratio  = ", (r2 / (r1 + r2)) * p[1] + (r1 / (r2 + r1)) * p[4])
print("Loss rate = ", p[0] + p[2] + p[3] + p[5])
