import scipy.io as sio
import numpy as np

appending_data = sio.loadmat('res.mat')
data = sio.loadmat('./iter5000/node2vec_res.mat')

graph_data = {
    'Attributes': np.zeros((3428, 155)),
    'Class': np.zeros((3428, 1), int),
    'Label': np.zeros((3428, 1), int),
    'Network': np.zeros((3428, 3428), int)
}
for i in range(len(data["Attributes"])):
    graph_data["Attributes"][i] = np.append(data["Attributes"][i], appending_data["Attributes"][i])

graph_data['Class'] = data["Class"]
graph_data['Label'] = data['Label']
graph_data['Network'] = data['Network']
sio.savemat('node2vec_res.mat', data)