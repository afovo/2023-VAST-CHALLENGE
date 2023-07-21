import json

import networkx as nx
from matplotlib import pyplot as plt

node_id_map = {}
node_map = {}
edgelist = []


def create_edgelist(json_data):
    nodes = json_data["nodes"]
    links = json_data["links"]

    node_id = 1

    for node in nodes:
        node_id_map[node["id"]] = node_id
        node_map[node_id] = node["id"]
        node_id += 1

    for link in links:
        source_id = node_id_map[link["source"]]
        target_id = node_id_map[link["target"]]
        G.add_edge(source_id, target_id, weight=link["weight"])
        # edgelist.append((source_id, target_id, link["weight"]))


with open("../data/MC1.json", "r") as file:
    json_data = json.load(file)
# 创建有向图
G = nx.MultiDiGraph()
# 创建edgelist
create_edgelist(json_data)

# 添加节点
G.add_nodes_from(node_id_map.values())

# 添加边
# G.add_edges_from(edgelist)
# nx.draw(G)
# plt.show()

# 定义自定义初始值
initial_values = {}
summ = len(node_id_map)
cnt = 0
for target in node_id_map:
    for key in node_id_map:
        if key == target:
            initial_values.update({node_id_map.get(key): 0.1})
        # if key == "Mar de la Vida OJSC":
        #     initial_values.update({node_id_map.get(key): 10})
        # elif key == "979893388":
        #     initial_values.update({node_id_map.get(key): 10})
        # elif key == "Oceanfront Oasis Inc Carriers":
        #     initial_values.update({node_id_map.get(key): 10})
        # elif key == "8327":
        #     initial_values.update({node_id_map.get(key): 10})
        else:
            initial_values.update({node_id_map.get(key): 0})

    # 计算自定义初始值的PageRank
    pagerank = nx.pagerank(G, personalization=initial_values, alpha=0.9, max_iter=5000)

    a1 = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
    if node_map.get(a1[0][0])==target:
        cnt += 1
print(cnt/summ)


# sum = 0
# # 打印结果
# for node, score in a1:
#     print("Node:", node_map.get(node), "PageRank Score:", score)
#     sum += score
#
# print(sum)
