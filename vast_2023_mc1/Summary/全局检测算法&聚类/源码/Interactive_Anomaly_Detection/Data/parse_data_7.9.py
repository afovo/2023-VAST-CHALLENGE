import numpy as np
import scipy.io as sio
import pandas as pd
import json
import pickle

with open('forFrontEnd/MC1(dup).json', "r", encoding='utf-8') as r:
    data = json.load(r)# [json.loads(line.strip()) for line in r.readlines()]
# nodes:[len 3428]  links:  [len 11069]

# 2. 创建空字典
graph_data = {
    'Attributes': np.zeros((3428, 27)),
    'Class': np.zeros((3428, 1), int),
    'Label': np.zeros((3428, 1), int),
    'Network': np.zeros((3428, 3428), int)
}

nodeNeighbours = {}
links = {}


node_id_mapping = {}  # 用于映射节点名称到唯一ID的字典
current_id = 0

edge_type_mapping = {"membership": 0, "partnership": 1, "ownership": 2, "family_relationship": 3, None: 4}
node_type_mapping = {"person": 0, "organization": 1, "company": 2, "political_organization": 3, "location": 4,
                     "vessel": 5, "event": 6, "movement": 7, None: 8}
node_types = ["person","organization","company","political_organization","location","vessel","event", "movement", "unknown"]

country_mapping = {}
country_id = 0
suspicious = ["Mar de la Vida OJSC", '979893388', "Oceanfront Oasis Inc Carriers", '8328']
# 处理点数据
for node in data["nodes"]:
    if node['id'] not in node_id_mapping:
        node_id_mapping[node['id']] = current_id
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

    if nodeNeighbours.get(source_id) is not None:
        s = nodeNeighbours.get(source_id)
        s.add(target_id)
        nodeNeighbours.update({source_id: s})
    else:
        s = set()
        s.add(target_id)
        nodeNeighbours.update({source_id: s})
    if nodeNeighbours.get(target_id) is not None:
        s = nodeNeighbours.get(target_id)
        s.add(source_id)
        nodeNeighbours.update({target_id: s})
    else:
        s = set()
        s.add(source_id)
        nodeNeighbours.update({target_id: s})

    if links.get((source_id, target_id)) is not None:
        a = links.get((source_id, target_id))
        a.append(link.get('type'))
        links.update({(source_id, target_id): a})
    else:
        links.update({(source_id, target_id): [link.get('type')]})
    # 'Attributes': np.ndarray((3428, 28)),  # 0：出度/总边数  1,2，3，4，5，6, 7, 8, 9一阶邻居节点类型分布，
    #                                            # 10,11，12，13，14一阶入边类型分布
    #                                            # 15,16，17，18，19一阶出边类型分布
    #                                            # 20,21，22，23，24一阶之间连边的类型分布
    #                                              25  入边平均权重
    #                                              26  出边平均权重

    source_class = graph_data['Class'][source_id][0]
    target_class = graph_data['Class'][target_id][0]

    graph_data["Attributes"][source_id][1 + graph_data['Class'][target_id][0]] += 1  # 邻居类型分布
    graph_data["Attributes"][source_id][15 + edge_type_mapping[link.get('type')]] += 1  # 一阶出边类型分布

    graph_data["Attributes"][target_id][1 + graph_data['Class'][source_id][0]] += 1  # 邻居类型分布
    graph_data["Attributes"][target_id][10 + edge_type_mapping[link.get('type')]] += 1  # 一阶入边类型分布

    if link.get('weight') is not None:
        graph_data["Attributes"][target_id][25] += link.get('weight')
        graph_data["Attributes"][source_id][26] += link.get('weight')

# 'Attributes': np.ndarray((3428, 28)),  # 0：出度/总边数  1,2，3，4，5，6, 7, 8, 9一阶邻居节点类型分布，
#                                            # 10,11，12，13，14一阶入边类型分布
#                                            # 15,16，17，18，19一阶出边类型分布
#                                            # 20,21，22，23，24一阶之间连边的类型分布
#                                              25  入边平均权重
#                                              26  出边平均权重
for nodeID in range(3428):
    attribute = graph_data["Attributes"][nodeID]
    if attribute[25] != 0 or attribute[26] != 0:
        inLinkCnt = np.sum(attribute[10:15])
        outLinkCnt = np.sum(attribute[15:20])
        attribute[0] = outLinkCnt / (inLinkCnt+outLinkCnt)
        neighbourCnt = np.sum(attribute[1:10])
        for ind in range(1, 10):
            attribute[ind] = attribute[ind] / neighbourCnt
        if inLinkCnt != 0:
            attribute[25] /= inLinkCnt
            for ind in range(10, 15):
                attribute[ind] = attribute[ind] / inLinkCnt
        if outLinkCnt != 0:
            attribute[26] /= outLinkCnt
            for ind in range(15, 20):
                attribute[ind] = attribute[ind] / outLinkCnt

        nlinkCnt = 0
        for neighbour in nodeNeighbours.get(nodeID):
            if links.get((nodeID, neighbour)) is not None:
                for linkT in links.get((nodeID, neighbour)):
                    attribute[20 + edge_type_mapping[linkT]] += 1
                    nlinkCnt += 1
            if links.get((neighbour, nodeID)) is not None:
                for linkT in links.get((neighbour, nodeID)):
                    attribute[20 + edge_type_mapping[linkT]] += 1
                    nlinkCnt += 1

        for ind in range(20, 24):
            attribute[ind] = attribute[ind] / nlinkCnt
sio.savemat('res.mat', graph_data)
# json.dump(parallelData, open('parallelData.json', 'w'))
