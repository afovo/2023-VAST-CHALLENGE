import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import pandas as pd




# 读取csv文件
df = pd.read_csv('merged_info.csv')
sdf = df[df["source"] == '979893388']
tdf = df[df["target"] == '979893388']
# 统计邻居同类型重边数量
scount = sdf.groupby(['link_type', 'target']).size().reset_index(name='count')
df1 = pd.DataFrame()
df1['name'] = scount['link_type'].str.cat(scount['target'], sep='\n')
df1['out count'] = scount['count']
fig, ax = plt.subplots()

tcount = tdf.groupby(['link_type', 'source']).size().reset_index(name='count')
df2 = pd.DataFrame()
df2['name'] = tcount['link_type'].str.cat(tcount['source'], sep='\n')
df2['in count'] = tcount['count']

res = pd.merge(df1, df2, how="outer", on="name").fillna(0)
res = res[res["in count"]+res["out count"] > 1]
ax.bar(res['name'], res['out count'], width=0.3, label='out count')
ax.bar(res['name'], res['in count'], bottom=res['out count'], width=0.3, label='in count')
ax.legend()
plt.show()

