# Summary

## IUU量化指标

肉眼看到一些表现怪异的：

​	怪核心

​	邻居成双向重边，构成多边形

### **同类型节点的邻居特征值**【wjf】

[距离之差]

TODO：

1. 分成点类型是organization和undefined的图，把同类型的用一个颜色画
2. 有重边（key>0)的节点的图
3. 特征值做百分比【出度入度之比，邻居类型占比，直连边类型占比，边平均权重】
4. 每个指标的中位数&平均数

![](\img\parallel.png)

### **有可疑点在的环长+环里可疑点的数目**【cl】



1. 把多环共用的边加粗，用输出样式把它画得更规整
2. <u>已知异常点所在环经过其它点的count</u>比较多的进行一个画
3. **考虑在图里点亮环**

==》Mar del Oeste Pic， Spanish Shimp Carrier在979893388 和 8327的各个级别环上频繁出现



### 国家间关系（船）【ldy】

==》19强连通分量+4直连细粒度分析：19艘连到可疑点的最短路上边的类型？共同经过的点最多的几个？

<img src="\img\ships.png" style="zoom:50%;" /> 

<img src="\img\country.png" style="zoom:33%;" /> 

通过ownership溯源过程中是否经过异常点？最短路图√

关键的船？有无国籍？



### 连通分量分离/合并

21个强（任两个点都可达）连通分量，除了Oceanfront Oasis Inc Carriers，其他三个可疑点都在837个成员的强连通分量里

83个弱连通分量，四个可疑点都在最大的分量里

**TODO:**

把<u>family</u>/<u>ownership</u>/<u>membership</u>相连的同类型点合成再画network



### 三元组 (点A，边，点B）排列组合的类型【txy】

（直接看好像看不出来）

1. 同类型双向重边

   - 所有边类型一共295对，全都在最大的强连通分量里
     - 和可疑点直接相连的有11对
     - 和可疑环产出点直接相连的有76
   - ownership, parnership一共有147对

2. 多角重边

   (所有边类型)长度为三的有80个

   sh rn y Corporation 拥有ping xi Line

   <img src="\img\新建文件夹\屏幕截图 2023-07-10 225756.jpg" style="zoom:30%;" /> 

3. 排列组合里不正常的组合在图里的占比

   e.g.

   <img src="\img\Q1\97983888\Calvin Salas.png" style="zoom:33%;" /> 

4. ---想想还有什么可拓展的



## 算法结果

### 聚类：KMEANS（层次聚类DBSCAN）

<img src="\img\Kmeans_.png" style="zoom:25%;" /> 

### Community detection【yf】

TODO：

把可疑点所在的社区画一下啥的

<img src="\img\community.png" style="zoom:33%;" /> 

### Hybrid Method: autoencoder and multi-view contrastive learning

重新跑出个结果

### Interactive reinforcement learning: GraphUCB algorithm

重新跑出个结果

### deepwalk，Line等graph embedding

出一个新的mat+点类型采样【wjf】

LINE:

```
if key == "Mar de la Vida OJSC":
    f.write(str(node_id_map.get(key)) + ' 1' + '\n')
elif key == "979893388":
    f.write(str(node_id_map.get(key)) + ' 2' + '\n')
elif key == "Oceanfront Oasis Inc Carriers":
    f.write(str(node_id_map.get(key)) + ' 3' + '\n')
elif key == "8327":
    f.write(str(node_id_map.get(key)) + ' 4' + '\n')
```



### pagerank

<img src="\img\pagerank.jpg" style="zoom:33%;" /> 

### *迪杰斯特拉



## 技术储备

- 平行坐标系统
- hierarchical-edge-bundling
- 时序ego-net
- networkx

## 数据处理

- id全变成字符串，string与int重复的在string前面加了“dup”
- 同类型同方向的重边weight相加绘图



## 可疑点

- 'Spanish Shrimp  Carriers'
- 'Faroe Islands Shrimp Shark'
- 'b8567859-bf54-49fd-8332-5775e19c65af'
- 'Mar del Oeste Pic'
- 'SeaSpray Wave SRL Solutions'
- 'png xi  Line'
- '7505050'
- '435054320'
- '160'



## TODO

**船：**通过ownership溯源过程中是否经过异常点？最短路图√  关键的船？有无国籍？【ldy】

**多角多边组合：**ownership, membership类型的环再看一眼（感觉这个双向会比较奇怪）；瞄一眼排列组合里不正常的组合【txy】

**成团简化：**把<u>family</u>/<u>ownership</u>/<u>membership</u>相连的<u>同类型点</u>合成一团再画network【cl】

**全局检测算法**：出一个新的embedding+点类型采样mat再跑一遍【wjf】

**数据故事构思**：【pny】

**技术完善**： 【yf】

1. 979893388的邻居可疑点Oceanfront没有颜色

2. 拖拽的时候有些边会抖（双击要不还是加回来吧
3. 邻居点类型筛选不了555

<u>这次摸索完就全力搭系统，7.18全部搞完！</u>