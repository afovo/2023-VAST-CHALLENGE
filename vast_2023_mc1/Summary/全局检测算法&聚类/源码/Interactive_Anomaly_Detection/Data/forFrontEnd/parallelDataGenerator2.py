import numpy as np
import scipy.io as sio
import pandas as pd
import json
import pickle

with open('MC1(dup).json', "r", encoding='utf-8') as r:
    data = json.load(r)# [json.loads(line.strip()) for line in r.readlines()]
# nodes:[len 3428]  links:  [len 11069]

# 2. 创建空字典
parallelData_raw = [np.zeros((3428, 29)), np.zeros((3428, 29)), np.zeros((3428, 29)), np.zeros((3428, 29)),
                    np.zeros((3428, 29)), np.zeros((3428, 29)), np.zeros((3428, 29)), np.zeros((3428, 29)),
                    np.zeros((3428, 29))]
nodeClass = np.zeros((3428, 1), int)
nodeNeighbours = {}
links = {}
parallelData = {"person": {},
                "organization": {},
                "company": {},
                "political_organization": {},
                "location": {},
                "vessel": {},
                "event": {},
                "movement": {},
                "null": {}}

node_id_mapping = {}  # 用于映射节点名称到唯一ID的字典
current_id = 0

edge_type_mapping = {"membership": 0, "partnership": 1, "ownership": 2, "family_relationship": 3, None: 4}
node_type_mapping = {"person": 0, "organization": 1, "company": 2, "political_organization": 3, "location": 4,
                     "vessel": 5, "event": 6, "movement": 7, None: 8}
node_types = ["person","organization","company","political_organization","location","vessel","event", "movement", "null"]

country_mapping = {}
country_id = 0
suspicious = ["Mar de la Vida OJSC", 979893388, "Oceanfront Oasis Inc Carriers", 8328]
# 处理点数据
for node in data["nodes"]:
    if node['id'] not in node_id_mapping:
        node_id_mapping[node['id']] = current_id
        current_id += 1
    if node.get('country') not in country_mapping:
        country_mapping[node.get('country')] = country_id
        country_id += 1

    node_id = node_id_mapping[node['id']]  # 当前node的数字化id
    nodeClass[node_id] = node_type_mapping[node.get('type')]
# 处理边数据
for link in data["links"]:
    source_id = node_id_mapping[link['source']]
    target_id = node_id_mapping[link['target']]

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
    # 'Attributes': np.ndarray((3428, 28)),  # 0：出度    1:入度  2，3，4，5，6, 7, 8, 9，10一阶邻居节点类型数，
    #                                            # 11，12，13，14，15一阶入边类型数
    #                                            # 16，17，18，19，20一阶出边类型数
    #                                            # 21，22，23，24，25一阶之间连边的类型数
    #                                              26  入边平均权重
    #                                              27  出边平均权重
    #                                              28  name

    source_class = nodeClass[source_id][0]
    target_class = nodeClass[target_id][0]

    parallelData_raw[source_class][source_id][0] += 1 # 出度
    parallelData_raw[target_class][target_id][1] += 1 # 入度

    parallelData_raw[source_class][source_id][2 + nodeClass[target_id][0]] += 1  # 邻居类型分布
    parallelData_raw[source_class][source_id][16 + edge_type_mapping[link.get('type')]] += 1  # 一阶出边类型分布

    parallelData_raw[target_class][target_id][2 + nodeClass[source_id][0]] += 1  # 邻居类型分布
    parallelData_raw[target_class][target_id][11 + edge_type_mapping[link.get('type')]] += 1  # 一阶入边类型分布

    if link.get('weight') is not None:
        parallelData_raw[target_class][target_id][26] += link.get('weight')
        parallelData_raw[source_class][source_id][27] += link.get('weight')

for i in range(9):
    # 'Attributes': np.ndarray((3428, 28)),  # 0：出度    1:入度  2，3，4，5，6, 7, 8, 9，10一阶邻居节点类型数，
    #                                            # 11，12，13，14，15一阶入边类型数
    #                                            # 16，17，18，19，20一阶出边类型数
    #                                            # 21，22，23，24，25一阶之间连边的类型数
    #                                              26  入边平均权重
    #                                              27  出边平均权重
    #                                              28  name
    for nodeID in range(3428):
        attribute = parallelData_raw[i][nodeID]
        if nodeID == 3172:
            print(attribute)
        if attribute[26] != 0 or attribute[27] != 0:
            inLinkCnt = np.sum(attribute[11:16])
            outLinkCnt = np.sum(attribute[16:21])
            neighbourCnt = np.sum(attribute[2:11])
            if inLinkCnt != 0:
                attribute[26] /= inLinkCnt
            if outLinkCnt != 0:
                attribute[27] /= outLinkCnt

            nlinkCnt = 0
            for neighbour in nodeNeighbours.get(nodeID):
                if links.get((nodeID, neighbour)) is not None:
                    for linkT in links.get((nodeID, neighbour)):
                        attribute[21 + edge_type_mapping[linkT]] += 1
                        nlinkCnt += 1
                if links.get((neighbour, nodeID)) is not None:
                    for linkT in links.get((neighbour, nodeID)):
                        attribute[21 + edge_type_mapping[linkT]] += 1
                        nlinkCnt += 1

            a = attribute.tolist()
            a[-1] = data["nodes"][nodeID]['id']

            parallelData[node_types[i]].update({a[-1]: a})
for i in range(9):
    a = parallelData_raw[i][~np.all(parallelData_raw[i]==0,axis=1)]
    avg = np.mean(a,axis=0).tolist()

    std = np.std(a,axis=0)
    threshold1 = np.maximum(avg - 3*std,0).tolist()
    threshold2 = np.maximum(avg + 3*std,0).tolist()

    avg[-1] = "Average"
    parallelData[node_types[i]].update({"AVG": avg})

    threshold1[-1] = "Threshold1"
    parallelData[node_types[i]].update({"Threshold1": threshold1})
    threshold2[-1] = "Threshold2"
    parallelData[node_types[i]].update({"Threshold2": threshold2})

json.dump(parallelData, open('parallelData2.json', 'w'))
