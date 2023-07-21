import json

node_id_map = {}
node_reverse_id_map = {}


def create_edgelist(json_data):
    nodes = json_data["nodes"]
    links = json_data["links"]

    edgelist = []
    node_id = 1

    for node in nodes:
        node_id_map[node["id"]] = node_id
        node_reverse_id_map[node_id] = node["id"]
        node_id += 1
        if node.get("country") is not None:
            print(node.get("country"))

    for link in links:
        source_id = node_id_map[link["source"]]
        target_id = node_id_map[link["target"]]
        edgelist.append((source_id, target_id))

    return edgelist


# 读取JSON文件
with open("MC1(dup).json", "r") as file:
    json_data = json.load(file)

# 创建edgelist
edgelist = create_edgelist(json_data)

with open("edgelist.txt", "w") as f:
    for edge in edgelist:
        f.write(str(edge[0]) + ' ' + str(edge[1]) + '\n')

with open("labels.txt", "w") as f:
    for key in node_id_map:
        if key == "Mar de la Vida OJSC":
            f.write(str(node_id_map.get(key)) + ' 1' + '\n')
        elif key == "979893388":
            f.write(str(node_id_map.get(key)) + ' 2' + '\n')
        elif key == "Oceanfront Oasis Inc Carriers":
            f.write(str(node_id_map.get(key)) + ' 3' + '\n')
        elif key == "8327":
            f.write(str(node_id_map.get(key)) + ' 4' + '\n')
        else:
            f.write(str(node_id_map.get(key)) + ' 0' + '\n')

json.dump(node_reverse_id_map, open('node_reverse_id_map.json', 'w'))
# # 打印edgelist
# for edge in edgelist:
#     print(edge[0], edge[1])
