import csv
import pandas as pd
from pyecharts.charts import Bar

file=pd.read_csv('multi_edge_neighbor.csv')
for i in file:
    print(i)
