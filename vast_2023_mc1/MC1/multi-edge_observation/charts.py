import csv
import numpy as np
import pandas as pd
from pyecharts.charts import Bar,Grid
from pyecharts import options as opts
from pyecharts.globals import  ThemeType

# grid = Grid(init_opts=opts.InitOpts(width=1200,height=720)) # 初始化，参数可传page_title,width,height
file=pd.read_csv('multi_edge_neighbor.csv')

x=file['cor_node'].values.tolist()
# print(x)
for idx,i in enumerate(file):
    attr=file[i].values.tolist()
    # print(attr)
    bar=Bar()
    bar.add_xaxis(x)
    bar.add_yaxis(i,attr)
    # bar.add(i,x,attr)
    bar.set_global_opts(title_opts=opts.TitleOpts(title="type: "+str(i)))
    # if idx%2==0:
    # distance=idx*100
    # distance=str(distance)+'%'
    bar.render('./html_charts/'+str(i)+'.html')




# from pyecharts.charts import Bar
# from pyecharts import options as opts

# data_test=[114, 55, 27, 101, 125, 27, 105]
# # V1 版本开始支持链式调用
# bar = (
#     Bar()
#     .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
#     .add_yaxis("商家A", data_test)
#     .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
#     .set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
# )
# bar.render()

# # 不习惯链式调用的开发者依旧可以单独调用方法
# bar = Bar()
# bar.add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
# bar.add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
# bar.add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
# bar.set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
# bar.render()