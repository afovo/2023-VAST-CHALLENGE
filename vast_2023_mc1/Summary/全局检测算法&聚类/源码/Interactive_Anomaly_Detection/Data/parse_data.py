import numpy as np
import scipy.io as sio
import pandas as pd
import json

# 1. 加载CSV文件并解析数据
data = pd.read_csv('MC1.csv', encoding_errors='ignore')

# 2. 创建空字典
graph_data = {
    'attributes': np.ndarray((3428, 6)),
    'class': np.ndarray((3428, 1)),
    'label': np.ndarray((3428, 1)),
    'network': np.ndarray((3428, 3428))
}

node_id_mapping = {}  # 用于映射节点名称到唯一ID的字典
current_id = 0

edge_type_mapping = {"membership": 0, "partnership": 1, "ownership": 2, "family_relationship": 3, np.nan: 8}
node_type_mapping = {"person": 0, "organization": 1, "company": 2, "political_organization": 3, "location": 4,
                     "vessel": 5, "event": 6, "movement": 7, np.nan: 8}

country_mapping = {}
country_id = 0

# 3. 遍历CSV数据
for row in data.iterrows():
    edge_type, weight, source, target, key, target_type, target_country, source_type, source_country = row[1]

    # 4. 添加源节点到字典
    if source not in node_id_mapping:
        node_id_mapping[source] = current_id
        current_id += 1

    # 4. 添加目标节点到字典
    if target not in node_id_mapping:
        node_id_mapping[target] = current_id
        current_id += 1

    if source_country not in country_mapping:
        country_mapping[source_country] = country_id
        country_id += 1

    if target_country not in country_mapping:
        country_mapping[target_country] = country_id
        country_id += 1

    # 5. 构建邻接矩阵图
    source_id = node_id_mapping[source]
    target_id = node_id_mapping[target]

    # if len(graph_data['network']) <= max(source_id, target_id):
    #     # 将邻接矩阵图的大小调整为适应新节点
    #     extend_size = max(source_id, target_id) - len(graph_data['network']) + 1
    #     graph_data['network'].extend([[] for _ in range(extend_size)])

    graph_data['network'][source_id][target_id] += 1

    # 6. 添加节点的特征信息
    attributes = [weight, key, node_type_mapping[target_type], country_mapping[target_country],
                  node_type_mapping[source_type], country_mapping[source_country]]
    graph_data['attributes'][target_id] = attributes

    attributes1 = [weight, key, node_type_mapping[source_type], country_mapping[source_country],
                   node_type_mapping[target_type], country_mapping[target_country]]
    graph_data['attributes'][source_id] = attributes

    # 7. 添加节点的类型信息
    node_class = edge_type  # 根据需要设置节点的类型
    graph_data['class'][source_id] = node_type_mapping[source_type]
    graph_data['class'][target_id] = node_type_mapping[target_type]

    # 8. 添加节点的异常标记信息
    if source_id in ("Mar de la Vida OJSC", 979893388, "Oceanfront Oasis Inc Carriers", 8327):
        graph_data['label'][source_id] = 1
    else:
        graph_data['label'][source_id] = 0

    if target_id in ("Mar de la Vida OJSC", 979893388, "Oceanfront Oasis Inc Carriers", 8327):
        graph_data['label'][target_id] = 1
    else:
        graph_data['label'][target_id] = 0

print(graph_data)
# 9. 保存为MAT文件
# sio.savemat('MC1.mat', graph_data)
json.dump(graph_data, open('graph_data.json', 'w'))
