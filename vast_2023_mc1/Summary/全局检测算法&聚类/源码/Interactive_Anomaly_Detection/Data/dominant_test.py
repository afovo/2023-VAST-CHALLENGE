# from pygod.detector import DOMINANT
from torch.utils.data import random_split
from torch_geometric.data import Data
import numpy as np
import networkx as nx
import scipy.sparse as sp
import torch
import torch.nn as nn
import scipy.io as sio
import random
import pygod.detector as det


# def dense_to_one_hot(labels_dense, num_classes):
#     """Convert class labels from scalars to one-hot vectors."""
#     num_labels = labels_dense.shape[0]
#     index_offset = np.arange(num_labels) * num_classes
#     labels_one_hot = np.zeros((num_labels, num_classes))
#     labels_one_hot.flat[index_offset+labels_dense.ravel()] = 1
#     return labels_one_hot


def load_mat(dataset, train_rate=0.7):
    data = sio.loadmat(dataset)
    label = data['Label'] if ('Label' in data) else data['gnd']
    attr = data['Attributes'] if ('Attributes' in data) else data['X']
    network = data['Network'] if ('Network' in data) else data['A']
    edge_index = data['edge_index'] if ('edge_index' in data) else data['edge']

    adj = sp.csr_matrix(network)
    feat = sp.lil_matrix(attr)

    # labels = np.squeeze(np.array(data['Class'], dtype=np.int64) - 1)
    # num_classes = np.max(labels) + 1
    # labels = dense_to_one_hot(labels, num_classes)

    # ano_labels = np.squeeze(np.array(label))

    # str_ano_labels = None
    # attr_ano_labels = None

    num_node = adj.shape[0]
    num_train = int(num_node * train_rate)
    # num_val = int(num_node * val_rate)
    all_idx = list(range(num_node))
    random.shuffle(all_idx)
    idx_train = all_idx[: num_train]
    # idx_val = all_idx[num_train : num_train + num_val]
    idx_test = all_idx[num_train:]
    test=edge_index[0]*edge_index[1]
    print(edge_index[0].shape, edge_index[1].shape,test.shape)

    return adj, feat, label, idx_train, idx_test, edge_index




if __name__=="__main__":

    # 注释掉的是原数据，edge index可能要改一下，下面的是小小图测试数据

    # adj, feat, label, train_data, test_dat, edge_index = load_mat("./MC1.mat")
    # x = torch.tensor(feat.toarray(), dtype=torch.float).contiguous()
    # train_x, test_x = x[:2400], x[2400:]
    # edge_index = torch.tensor(edge_index, dtype=torch.long).contiguous()
    # # train_edge_index, test_edge_index = adj[:2400], adj[2400:]
    # train_edge_index, test_edge_index = edge_index[:2400], edge_index[2400:]
    # train_data = Data(x=train_x, edge_index=train_edge_index)
    # # train_data = Data(x=train_x)
    # # node labels
    # y = torch.tensor(label, dtype=torch.long)
    # train_data.y = y[:2400]

    # test_data = Data(x=test_x, edge_index=test_edge_index)
    # # test_data = Data(x=test_x)
    # test_data.y = y[2400:] 

    x = torch.tensor(([[3,1],[2,2],[1,1],[0,0],[1,1]]), dtype=torch.float).contiguous()
    train_x, test_x = x[:3], x[3:]
    train_edge_index=[[0,0,1,2],[1,1,2,0]]
    test_edge_index=[[0,1],[4,4]]
    train_edge_index = torch.tensor(train_edge_index, dtype=torch.long).contiguous()
    test_edge_index = torch.tensor(test_edge_index, dtype=torch.long).contiguous()
    # train_edge_index, test_edge_index = adj[:2400], adj[2400:]
    # train_edge_index, test_edge_index = edge_index[:,0,1,4,5], edge_index[:,2,3]
    train_data = Data(x=train_x, edge_index=train_edge_index)
    # train_data = Data(x=train_x)
    # node labels
    label=[0,0,0,0,1]
    y = torch.tensor(label, dtype=torch.long)
    train_data.y = y[:3]

    test_data = Data(x=test_x, edge_index=test_edge_index)
    # test_data = Data(x=test_x)
    test_data.y = y[3:] 
    # print(test_data.y)

    # print(train_data.is_undirected())
    model = det.CoLA()  # hyperparameters can be set here
    model.fit(train_data)  # input data is a PyG data object

    # get outlier scores on the training data (transductive setting)
    score = model.decision_score_

    # predict labels and scores on the testing data (inductive setting)
    pred, score = model.predict(test_data, return_score=True)
    print(pred)
