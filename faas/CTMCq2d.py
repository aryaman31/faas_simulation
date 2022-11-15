import numpy as np 

data = np.loadtxt("../trace-final.csv", skiprows=1, delimiter=',', dtype=int)
time = 30 * 24 * 60 * 60 # in seconds
np.set_printoptions(suppress=True)


r1, s1 = data[0, 1] / time, 1 / data[0, 2]
r2, s2 = data[1, 1] / time, 1 / data[1, 2]
a = 0.5
genMatrix = np.array([[-s1, s1      ,  0, 0  , 0       , 0 , 1],
                      [r1 , -(r1+r2), 0 , 0  , 0       , r2, 1],
                      [a  , 0       , -a, 0  , 0       , 0 , 1],
                      [0  , 0       , 0 , -s2, s2      , 0 , 1],
                      [0  , 0       , r1, r2 , -(r1+r2), 0 , 1],
                      [0  , 0       , 0 , a  , 0       , -a, 1]], dtype=float)
b = np.array([[0], [0], [0], [0], [0], [0], [1]])
genMatrixT = np.transpose(genMatrix)
print(genMatrixT.shape)
pt = np.linalg.lstsq(np.transpose(genMatrix), b)[0]
print(pt)
