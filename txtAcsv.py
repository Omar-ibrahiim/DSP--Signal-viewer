import numpy as np

def txt(filename):
    data = np.loadtxt(filename, delimiter=',')
    return data