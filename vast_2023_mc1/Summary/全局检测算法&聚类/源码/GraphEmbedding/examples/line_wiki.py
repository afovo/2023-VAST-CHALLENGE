
import numpy as np

from ge.classify import read_node_label, Classifier
from ge import LINE
from sklearn.linear_model import LogisticRegression
import json

import scipy.io as sio
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.manifold import TSNE


def evaluate_embeddings(embeddings):
    X, Y = read_node_label('../data/labels.txt')
    tr_frac = 0.8
    print("Training classifier using {:.2f}% nodes...".format(
        tr_frac * 100))
    clf = Classifier(embeddings=embeddings, clf=LogisticRegression())
    clf.split_train_evaluate(X, Y, tr_frac)


def plot_embeddings(embeddings,):
    X, Y = read_node_label('../data/labels.txt')

    emb_list = []
    for k in X:
        emb_list.append(embeddings[k])
    emb_list = np.array(emb_list)

    model = TSNE(n_components=2)
    node_pos = model.fit_transform(emb_list)

    color_idx = {}
    for i in range(len(X)):
        color_idx.setdefault(Y[i][0], [])
        color_idx[Y[i][0]].append(i)

    for c, idx in color_idx.items():
        plt.scatter(node_pos[idx, 0], node_pos[idx, 1], label=c)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    G = nx.read_edgelist('../data/edgelist.txt',
                         create_using=nx.DiGraph(), nodetype=None, data=[('weight', int)])

    model = LINE(G, embedding_size=128, order='second')
    model.train(batch_size=1024, epochs=1000, verbose=2)
    embeddings = model.get_embeddings()

    graph_data = {
        'Attributes': np.zeros((3428, 128)),
        'Class': np.zeros((3428, 1), int),
        'Label': np.zeros((3428, 1), int),
        'Network': np.zeros((3428, 3428), int)
    }
    with open('../data/MC1(dup).json', "r", encoding='utf-8') as r:
        data = json.load(r)
    edge_type_mapping = {"membership": 0, "partnership": 1, "ownership": 2, "family_relationship": 3, None: 4}
    node_type_mapping = {"person": 0, "organization": 1, "company": 2, "political_organization": 3, "location": 4,
                         "vessel": 5, "event": 6, "movement": 7, None: 8}
    node_types = ["person", "organization", "company", "political_organization", "location", "vessel", "event",
                  "movement", "unknown"]

    country_mapping = {}
    country_id = 0
    suspicious = ["Mar de la Vida OJSC", 979893388, "Oceanfront Oasis Inc Carriers", 8328]
    node_id_mapping = {}  # 用于映射节点名称到唯一ID的字典
    node_reverse_id_map = {}
    current_id = 0
    # 处理点数据
    for node in data["nodes"]:
        if node['id'] not in node_id_mapping:
            node_id_mapping[node['id']] = current_id
            node_reverse_id_map[current_id] = node["id"]
            current_id += 1
        if node.get('country') not in country_mapping:
            country_mapping[node.get('country')] = country_id
            country_id += 1

        node_id = node_id_mapping[node['id']]  # 当前node的数字化id
        graph_data['Class'][node_id] = node_type_mapping[node.get('type')]

        if node['id'] in suspicious:  # "Mar de la Vida OJSC":  #, 979893388, "Oceanfront Oasis Inc Carriers", 8327
            graph_data['Label'][node_id] = 1
        else:
            graph_data['Label'][node_id] = 0

    # 处理边数据
    for link in data["links"]:
        source_id = node_id_mapping[link['source']]
        target_id = node_id_mapping[link['target']]
        graph_data['Network'][source_id][target_id] += 1


    for key in embeddings:
        graph_data["Attributes"][int(key)-1] = embeddings[key]


    emb_list = graph_data["Attributes"]

    model = TSNE(n_components=2)
    node_pos = model.fit_transform(emb_list)

    res = []

    for i in range(len(node_pos)):
        res.append([float(node_pos[i][0]), float(node_pos[i][1]), node_reverse_id_map[i]])
    json.dump(res, open('res1.json', 'w'))

    # print(graph_data["Attributes"])
    # sio.savemat('line_res.mat', graph_data)
    evaluate_embeddings(embeddings)
    plot_embeddings(embeddings,)
