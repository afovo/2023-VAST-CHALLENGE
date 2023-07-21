import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import pandas as pd
import json
import pickle

with open('MC1.json', "r", encoding='utf-8') as r:
    dics = [json.loads(line.strip()) for line in r.readlines()]
# 1. 加载CSV文件并解析数据
data = dics[0]  # nodes:[len 3428]  links:  [len 11069]
suspicious = ["Mar de la Vida OJSC", 979893388, "Oceanfront Oasis Inc Carriers", 8327]

# 读取csv文件
df = pd.read_csv('merged_info.csv')
cnt = 0
all = len(data['nodes'])

for node in data['nodes']:
    sdf = df[df["source"] == node['id']]
    tdf = df[df["target"] == node['id']]
    # 统计邻居同类型重边数量
    scount = sdf.groupby(['link_type', 'target']).size().reset_index(name='count')
    df1 = pd.DataFrame()
    df1['name'] = scount['link_type'].str.cat(scount['target'], sep='\n')
    df1['out count'] = scount['count']
    # fig, ax = plt.subplots()

    tcount = tdf.groupby(['link_type', 'source']).size().reset_index(name='count')
    df2 = pd.DataFrame()
    df2['name'] = tcount['link_type'].str.cat(tcount['source'], sep='\n')
    df2['in count'] = tcount['count']

    res = pd.merge(df1, df2, how="outer", on="name").fillna(0)
    res = res[res["in count"] + res["out count"] > 1]
    if len(res) > 0:
        cnt += 1
        print(node['id'])
    # ax.bar(res['name'], res['out count'], width=0.3, label='out count')
    # ax.bar(res['name'], res['in count'], bottom=res['out count'], width=0.3, label='in count')
    # ax.legend()
    # plt.show()

print(cnt / all)
