import networkx as nx

# 创建有向图
G = nx.DiGraph()

# 添加节点
G.add_nodes_from([1, 2, 3, 4])

# 添加边
G.add_edges_from([(1, 2), (2, 1), (1, 3), (3, 1), (4, 1)])

# 定义自定义初始值
initial_values = {1: 0, 2: 0, 3: 0, 4: 1000}

# 计算自定义初始值的PageRank
pagerank = nx.pagerank(G, personalization=initial_values)

# 打印结果
for node, score in pagerank.items():
    print("Node:", node, "PageRank Score:", score)
