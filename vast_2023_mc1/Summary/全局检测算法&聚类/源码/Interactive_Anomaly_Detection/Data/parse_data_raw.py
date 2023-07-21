import numpy as np
import scipy.io as sio
import pandas as pd
import json
import pickle

with open('MC1.json', "r", encoding='utf-8') as r:
    dics = [json.loads(line.strip()) for line in r.readlines()]
# 1. 加载CSV文件并解析数据
data = dics[0]  # nodes:[len 3428]  links:  [len 11069]

# 2. 创建空字典
graph_data = {
    'Attributes': np.zeros((3428, 17)),  # 0：出度  1：入度   2，3，4，5，6一阶邻居节点类型分布，
    # 7，8，9，10，11，12，13，14，15一阶连边类型分布
    # 16 边权重之和
    'Class': np.zeros((3428, 1), int),
    'Label': np.zeros((3428, 1), int),
    'Network': np.zeros((3428, 3428), int)
}

node_id_mapping = {}  # 用于映射节点名称到唯一ID的字典
current_id = 0

edge_type_mapping = {"membership": 0, "partnership": 1, "ownership": 2, "family_relationship": 3, None: 4}
node_type_mapping = {"person": 0, "organization": 1, "company": 2, "political_organization": 3, "location": 4,
                     "vessel": 5, "event": 6, "movement": 7, None: 8}

country_mapping = {}
country_id = 0
suspicious=["Mar de la Vida OJSC", 979893388, "Oceanfront Oasis Inc Carriers", 8327]
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
    # 'Attributes': np.ndarray((3428, 16)),  # 0：出度  1：入度   2，3，4，5，6,7,8,9,10一阶邻居节点类型分布，
    #                                            # 11，12，13，14，15一阶连边类型分布（包含重边信息
    #                                              16  边平均权重
    graph_data["Attributes"][source_id][0] += 1
    graph_data["Attributes"][target_id][1] += 1
    graph_data["Attributes"][source_id][2 + graph_data['Class'][target_id][0]] += 1
    graph_data["Attributes"][source_id][11 + edge_type_mapping[link.get('type')]] += 1

    graph_data["Attributes"][target_id][2 + graph_data['Class'][source_id][0]] += 1
    graph_data["Attributes"][target_id][11 + edge_type_mapping[link.get('type')]] += 1

    # if link.get('weight') is not None:
    #     graph_data["Attributes"][target_id][16] += link.get('weight')

print(graph_data)

for i in range(9):
    c=np.sum(graph_data['Class']==i)
    print (str(i)+":  "+str(c)) #输出满足条件的个数


# 9. 保存为MAT文件
sio.savemat('MC1.mat', graph_data)
# json.dumps(graph_data, open('graph_data.json', 'w'))
for key in graph_data:
    graph_data[key] = graph_data[key].tolist()
json.dump(graph_data, open('graph_data.json', 'w'))
