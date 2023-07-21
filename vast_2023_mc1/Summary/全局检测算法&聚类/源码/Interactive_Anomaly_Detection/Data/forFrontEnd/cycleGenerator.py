# 建图

#%%
import datetime
import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import math

#%%
threshold = 1
limit = 6
included_node_types = {"person", "company", "organization", "political_organization", "vessel", "null"}

with open('MC1(dup).json', 'r') as file:
    json_data = json.load(file)
nodes = json_data['nodes']
node_type_dict = {}
links = json_data['links']

#%%
neighbors_dict = {}

# Step 1: Initialize neighbors_dict with empty lists for each node
for node in nodes:
    node_id = node['id']
    if node.get('type') is not None:
        node_type_dict[node_id] = node['type']
    else:
        node_type_dict[node_id] = "null"
    neighbors_dict[node_id] = set()  # [0]一阶邻居  [1]二阶邻居

# Step 2: Build connections between nodes
for link in links:
    source_node = link['source']
    target_node = link['target']
    neighbors_dict[source_node].add(target_node)
    neighbors_dict[target_node].add(source_node)

# Step 3: Get second-order neighbors for each node
for node in nodes:
    node_id = node['id']
    first_order_neighbors = neighbors_dict[node_id]
    second_order_neighbors = set()

    for neighbor in first_order_neighbors:
        second_order_neighbors = second_order_neighbors|neighbors_dict[neighbor]

    neighbors_dict[node_id] = first_order_neighbors|second_order_neighbors



G = nx.DiGraph()
edges = []
for link in links:
    edges.append((link['source'], link['target']))
edges = list(set(edges))
G.add_edges_from(edges)

#%%

suspects = ["979893388", "Oceanfront Oasis Inc Carriers"]

cycleData = {}

# 在指定长度内统计环的数量

#%%
def find_all_cycles(graph, start_node, num_steps):
    visited = set()
    all_paths = [[[],[0,0]], [[],[0]]]   #存1个(9, O)，2个(9+O)
    dfs_paths(graph, start_node, start_node, num_steps, visited, [], all_paths, [])
    return all_paths


def dfs_paths(graph, start_node, current_node, steps_left, visited, path, all_paths, suspect):
    suspect_copy = suspect.copy()
    if (current_node in suspects) and (current_node not in suspect):
        suspect_copy.append(current_node)

    if steps_left == 0 and current_node == start_node: # 找到了符合条件的环
        all_paths[len(suspect_copy)-1][0].append(path + [current_node])
        if len(suspect_copy) == 1:
            if suspect_copy[0] == "979893388":
                all_paths[0][1][0]+=1
            elif suspect_copy[0] == "Oceanfront Oasis Inc Carriers":
                all_paths[0][1][1]+=1
        elif len(suspect_copy) == 2:
            all_paths[1][1][0] += 1

    if current_node in visited or steps_left < 0 or node_type_dict[current_node] not in included_node_types:
        return  # 终止递归, 不添加进环列表
    visited.add(current_node)
    next_nodes = graph[current_node]
    for next_node in next_nodes:
        dfs_paths(graph, start_node, next_node, steps_left - 1, visited, path + [current_node], all_paths, suspect_copy)
    visited.remove(current_node)


def count_cycles(G, node, start_length, end_length):
    X = np.arange(start_length, end_length+1)
    count = [[], [], [], []]
    record = []
    for x in X:
        all_paths = find_all_cycles(G, node, x)  # [[], [], [], []]
        paths = []
        for i in range(len(all_paths)):
            paths.append(all_paths[i][0])
        record.append(paths)

        for i in range(len(paths)):
            count[i].append(all_paths[i][1])

    print("Details of count:")
    for i in range(len(count)):
        print(count[i])

    return count


def find_cycles(graph, node, order):
    # 筛选指定阶数邻居
    # 将有向图转为无向图
    graph = graph.to_undirected()

    # 获取节点列表
    neighbor_graph = nx.ego_graph(graph, node, radius = order,  undirected=True)
    neighbors = list(neighbor_graph.nodes())

    print(f"There are {len(neighbors)} neighbours. ({order})")

    # 指定阶数内的子图
    G_ego = nx.DiGraph()
    edges_ego = []
    for link in links:
        if link['source'] in neighbors and link['target'] in neighbors:
            edges_ego.append((link['source'], link['target']))
    G_ego.add_edges_from(edges_ego)

    # 指定阶数内的环列表
    cycles = nx.simple_cycles(G_ego)

    selected_cycles = []
    try:
        cycle = next(cycles)
        while cycle:
            if node in cycle:
                selected_cycles.append(cycle)
                #print(cycle)
            cycle = next(cycles, None)

    except StopIteration:
        print("There is no cycle.")

    return selected_cycles

def filter_nodes(arr, set_values):
    result = set()
    n = len(arr)
    i = 0

    while i < n:
        curr = arr[i]

        if curr in set_values:
            next_index = (i + 1) % n
            next_val = arr[next_index]

            if next_val in set_values:
                result.add(curr)
                result.add(next_val)

        i += 1

    return list(result)

def sort_cycle_data(cycle_data):
    sorted_dict = {}
    sorted_items = sorted(cycle_data.items(), key=lambda x: x[1]['count'], reverse=True)
    rank_counter = 0
    prev_count = None
    for key, value in sorted_items:
        if value['count'] != prev_count:
            rank_counter += 1
        value['rank'] = rank_counter
        sorted_dict[key] = value
        prev_count = value['count']
    return sorted_dict

def draw_cycles(G, node, length):
    startTime = datetime.datetime.now()
    paths = find_all_cycles(G, node, length)

    for i in range(2): # path[i][0]之和: 长度为length的所有环的数组
        for path in paths[i][0]:
            # if (datetime.datetime.now()-startTime).seconds > threshold:
            #     return
            path_nodes = set(path)
            for node_id in path[0:-1]:
                if node_id != node and node_type_dict[node_id] in included_node_types:
                    if cycleData.get(node_id) is not None:
                        if cycleData[node_id].get(length) is None: # 有这个点，但这个长度的环没记录过
                            cycleData[node_id].update({length: {"data":[],"lcount":0}})
                    else:  # 从没有过这个点
                        cycleData.update({node_id: {length: {"data":[],"lcount":0}, "count": 0, "rank":0}})
                    nodes_list = cycleData[node_id][length]["data"]

                    neighbour_path_nodes = path_nodes & neighbors_dict[node_id]
                    result = filter_nodes(list(neighbour_path_nodes), neighbors_dict[node_id])

                    nodes_list.extend(result)
                    cnt = cycleData[node_id]["count"] + 1
                    lcnt = cycleData[node_id][length]["lcount"] + 1
                    cycleData[node_id].update(
                        {length: {"data": nodes_list, "lcount":lcnt}, "count": cnt, "rank": 0})


for i in range(2):
    for j in range(2, limit+1):
        draw_cycles(G, suspects[i], j)   #'Spanish Shrimp  Carriers', '341411'  , include='435054320'


cycleData = sort_cycle_data(cycleData)
with open(f'res.json', 'w') as file:
   json.dump(cycleData, file)

