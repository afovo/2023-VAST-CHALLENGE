import pandas as pd
import matplotlib.pyplot as plt

# 读取csv文件
df = pd.read_csv('merged_info.csv')


# df = df.query("(source=='979893388'| target=='979893388')")
# 统计三个键值的组合数量
count = df.groupby(['link_type', 'source_type', 'target_type']).size().reset_index(name='count').query("(source_type=='location'| target_type=='location') & link_type=='partnership'")
a = count['link_type'].str.cat([count['source_type'], count['target_type']], sep=' ')
counts = count['count']
fig, ax = plt.subplots()
ax.bar(a, counts, width=0.3, label='count')
ax.legend()
plt.show()

print(count)
