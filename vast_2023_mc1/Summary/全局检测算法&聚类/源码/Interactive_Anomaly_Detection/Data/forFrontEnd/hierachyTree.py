import numpy as np
import scipy.io as sio
import pandas as pd
import json
import pickle

# 忽略反边的ownership层级
# 公司股权关系：在企业知识图谱中，"ownership"边可以表示公司之间的股权关系。例如，一家公司拥有另一家公司的股份，"ownership"边可以从拥有者指向被拥有者。
# （包括的点类型：company, organization, political_organization, vessel, person, unknown
with open('MC1(dup).json', "r", encoding='utf-8') as r:
    data = json.load(r)  # [json.loads(line.strip()) for line in r.readlines()]
# nodes:[len 3428]  links:  [len 11069]
suspicious = ["Mar de la Vida OJSC", 979893388, "Oceanfront Oasis Inc Carriers", 8327]
nodeTypes = ["company", "organization", "political_organization", "vessel", "person", None]

root = {
    'name': '8327',
    'type': 'organization',
    'children': [],
    '_children':[]
}

nodeClass = {}
ss = set()
nodeNeighbours = {}
links = {}


def addNodes(node):
    ss.add(node['name'])
    if nodeNeighbours.get(node['name']) is None:
        return
    for child in nodeNeighbours.get(node['name']):
        if  child in ss:
            continue
        node['children'].append({'name': child, 'children': [], '_children': []})
        node['_children'].append({'name': child, 'children': [], '_children': []})
        addNodes(node['children'][-1])

for node in data["nodes"]:
    nodeClass[node['id']] = node.get('type')# 处理边数据


for link in data["links"]:
    source = link['source']
    target = link['target']
    if link.get('type')=='ownership' and nodeClass[source] in nodeTypes and nodeClass[target] in nodeTypes:
        if nodeNeighbours.get(source) is not None:
            s = nodeNeighbours.get(source)
            s.add(target)
            nodeNeighbours.update({source: s})
        else:
            s = set()
            s.add(target)
            nodeNeighbours.update({source: s})
        if nodeNeighbours.get(target) is not None:
            s = nodeNeighbours.get(target)
            s.add(source)
            nodeNeighbours.update({target: s})
        else:
            s = set()
            s.add(source)
            nodeNeighbours.update({target: s})

addNodes(root)

json.dump(root, open('hierachyData_ownership_out.json', 'w'))
