import  numpy as np
import scipy.io as sio
def mat(filename):
    data=sio.loadmat(filename)
    for i in data:
        if '__' not in i and 'readme' not in i:
            np.savetxt(("./__pycache__/file.csv"),data[i],delimiter=',')
    data = np.loadtxt("./__pycache__/file.csv", delimiter=',')
    return data
