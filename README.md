# 2023 Vast Challenge 会议记录

## 学习笔记

### 腾讯文档link

[ChinaVis 破题 (qq.com)](https://docs.qq.com/doc/DRElLemNFU2Z4V2Z5?u=9ccd436263224792aed1e201d311483d)
【腾讯文档】VAST CHALLENGE 往届题 https://docs.qq.com/doc/DWE1SWGFWdFdveE5y

### 分工
| 任务         | 描述                        |  人    |
| ------------ | --------------------------- | ---- |
| 数据处理  |  |      |
| 开发+讲数据故事 | 构思并搭建框架，连接前后端                  |      |
| 前端     | 前端可视化          |      |
| 论文     |                             |      |
|              |                             |      |

### 破题Tips

1. 行业背景调研（专业用词、常识【e.g.营业时间】）
2. 列举不同维度的特征寻找关系（e.g.中文姓，男女对地区的偏好）
3. 客观事实（e.g.地理实际位置&商圈，身份证区号变化，老人上网时长）
4. 可视化信息量浓缩（拓扑图中节点大小表示流量）


### 数据处理流程Tips

#### 数据清洗

空键值

注意未提及的不合法数据（年龄等）

<u>？数据库</u>



### 技术栈

Vue   D3   Echarts

**可视化**

| 类别                  | API/图名                         |      |
| --------------------- | -------------------------------- | ---- |
| 拓扑图                | Gephi[API]<br>力导向图           |      |
| 统计多维度数据special | 切尔诺夫脸谱图<br>brush联动[API] |      |
|                       |                                  |      |
|                       |                                  |      |
|                       |                                  |      |

**算法**

| 用途         | 算法                        |      |
| ------------ | --------------------------- | ---- |
| 权重划分子图 | Fast Unfolding 社区发现算法 |      |
| 邮件分类     | NLP                         |      |
|              |                             |      |
|              |                             |      |
|              |                             |      |

## 时间线

| 周   | 开会时间  |      | 目标                                          |
| ---- | --------- | ---- | --------------------------------------------- |
| 15   | 5.25      |      | 部署系统，代码&UI整理，分配统计量和筛选器工作 |
| 16   | 6.1       |      | 完成剩余统计量可视化，开始图挖掘              |
| 17   | 6.8       |      | 完成筛选器功能，根据分析结果开始设计MC1系统   |
| 18   | 6.15      |      | MC1答案构思，MC2找思路，MC1系统搭建           |
| 19   | 6.22      |      |                                               |
| 20   | 6.29      |      |                                               |
| 21   | 7.12-7.13 |      | 7.13下午两点前交稿                            |
|      |           |      |                                               |



## 3.4
技术栈：dash+D3  (tableua) (R)

第一次答辩前：封装一个模块齐全的可视化大屏 ：)

**周一晚上**  7:30 一丹310



## 3.18

前端Vue+d3技术实现：看懂demo（群里陆陆），+d3

数据准备+建模+机器学习：都学

第一次答辩准备：写完proposal

**周四下午**  2：30  开始做黑网吧



## 3.23

<img src="C:\Users\afo\AppData\Roaming\Typora\typora-user-images\image-20230323155445411.png" alt="image-20230323155445411" style="zoom:67%;" />  <img src="C:\Users\afo\AppData\Roaming\Typora\typora-user-images\image-20230323155636560.png" alt="image-20230323155636560" style="zoom:67%;" /><img src="C:\Users\afo\AppData\Roaming\Typora\typora-user-images\image-20230323155607579.png" alt="image-20230323155607579" style="zoom:50%;" />

| 图                                                  | 人   | ddl               |
| --------------------------------------------------- | ---- | ----------------- |
| **地图**        折线图 柱状图 饼图 散点图 路径图    | wjf  | 3.30\|4.5         |
| **关系图**    K线图 雷达图 热力图 树图 矩形树图     | ll   | 3.30\|4.5         |
| **粒子动图** 旭日图 平行坐标系 桑基图 漏斗图 仪表盘 | ldy  | 3.30\|4.5(破题会) |

| 交互       | 人   |      |
| ---------- | ---- | ---- |
| 弹窗       |      |      |
| 全局的皮肤 |      |      |
| 组件排版   | wjf  | 3.24 |
| ppt        | ll   | 3.29 |
| 论文       | ldy  | 3.29 |


## 4.6
1. 分工
2. 比赛概览
3. 备赛计划

模拟题：2021  mini challenge2.4
| 任务       | 人   |  备注  |
| ---------- | ---- | ---- |
| *数据清洗+透视分析 |-| car-assignment.csv, gps.csv   |
| *数据故事设计+布局设计| - | 复现 |
| 地图可视化           | wjf  |      |
| 车辆轨迹可视化+calender | yf  | +gps.csv |
| 人物关系+聚集行为数据分析 | ldy  |      |
| 人物关系+聚集行为可视化 | txy  |      |
| 往届调研             | wjf, ldy, cl|         |
| 技术准备完善         | pny(tableu放网页), cl做关系图, wjf,ldy完善图库|      |



## 4.20

### 2021 MC2后半段复现

| 任务                      | 人                                             | 备注              | DDL  |
| ------------------------- | ---------------------------------------------- | ----------------- | ---- |
| 地图可视化                | wjf                                            | Three.js 帅气3D图 | 4.22 |
| 车辆轨迹可视化+calender   | yf                                             | +gps.csv   D3.js  | 4.27 |
| 人物关系+聚集行为数据分析 | ldy                                            | d3.js             | 4.27 |
| 人物关系+聚集行为可视化   | txy                                            | d3.js             | 4.27 |
| **往届调研**              | wjf, ldy, cl                                   | 3-6年             | 4.27 |
| 技术准备完善              | pny(tableu放网页), cl做关系图, wjf,ldy完善图库 |                   | 4.27 |

*如果发题了

| 任务              | 人           | 备注 | DDL  |
| ----------------- | ------------ | ---- | ---- |
| 看看数据          | pny          |      | 4.27 |
| 调研&技术准备完善 | wjf, ldy, cl |      | 4.27 |



### 往届调研

| 年份       | 人     | DDL                                                    |
| ---------- | ------ | ------------------------------------------------------ |
| 2022，2017 | 邬静芙 | 4.21（粗粒度，题->解法） \|  4.27（细粒度 需求->技术） |
| 2021，2018 | 陆荻芸 | 同上                                                   |
| 2020，2019 | 陈蕾   | 同上                                                   |

## 5.11 

### MC1

1. 题目分析

2. 分享EDA分析结果（e.g.各变量意义？type下都有什么？）【pny】
   - 图数据挖掘
   
   - 不太符合常见的分布——考虑做筛选看分布
   
     <img src="C:\Users\afo\AppData\Roaming\Typora\typora-user-images\image-20230511162101072.png" alt="image-20230511162101072" style="zoom:50%;" /> 
   
   - 
   
3. 技术栈统一，分配初步可视化知识图谱、调研、数据分析任务

   - netv.js
   - https://observablehq.com/@d3/hierarchical-edge-bundling
   - *gephi
   - *tulip

4. 确认整体时间线



### MC2

1. 题目分析
2. EDA
   - 图算法链路分析
3. aa



算法预测后对异常的故事解释

保证一个mc的任务量



### **任务分配**

| DDL  | Task                                                         | Member                                       |
| ---- | ------------------------------------------------------------ | -------------------------------------------- |
| 5.18 | 1. MC1,2 netv.js<br>2. hierarchical-edge-bundling知识图谱可视化，目标实体标注<br>3. 小图分开画，各维度数据分析<br>4. 调研 (知识图谱分析的先例，非法渔业指标，图数据挖掘) | 1. yf<br>2. wjf, txy<br>3. pny<br>4. ldy, ll |
| 5.25 | 1.  系统搭建，选中节点探索【1. 画suspected附近的邻居(1,2,3阶)  2. console+页面设计  3. 过滤出来画统计图+等pny需求】<br>2.  调研总结，IUU rule set；知识图谱挖掘&匹配算法继续调研<br>3.  每个节点类型下边类型的分布；数据清洗，探索+节点探索辅助；和知识图谱强相关的方法 | 1. yf, wjf, txy<br>2. ldy, ll<br>3. pny      |
|      |                                                              |                                              |
|      |                                                              |                                              |



## 5.18

### 数据分析

#### MC1

1. **node**：id有<u>重复值</u>   type缺失值很少[person和organization为主  ]，country有2/3缺失[某个占绝大部分]

   没有无国家个人

2. **edge**：没有缺失值，weight（基本都>0.8)【用途？关注一下小的】

（出度：主语；入度：宾语）

【ToDo: 每个节点类型下边类型的分布



##### **界面：d3**

   一阶二阶邻居   辅助节点关系探索

   搜索console（**node**： type， 关键字      ==》选中节点(suspecious point)为中心画ego-network      选到二阶邻居）

​			过滤条件：某个属性为某种类型



##### **调研**

![image-20230518165654982](C:\Users\afo\AppData\Roaming\Typora\typora-user-images\image-20230518165654982.png)

【ToDo: 记录IUU规则

 i.e. vessel 没有国籍信息值得怀疑【啊哦  全都没有国籍



对渔船危险程度的评估

可以用节点分类对未知类别的节点做标注

------



## 5.25

图相关：这四个异常点都不在outlier里

异常：统计量/动态过程
其它的同类型节点特征平均值
和一个节点有多条重边=>key 重边数 筛选一下

id语义相同的节点的连接特征

图里的clustering



isphere：映射到3D球展示

图挖掘算法

------



| Task【ddl】                                                  | Member |
| ------------------------------------------------------------ | ------ |
| 知识图谱数据挖掘                                             | pny    |
| 服务器部署+自动化构建【week16】                              | yf     |
| 代码整理+debug（`性能提升`）【week16】                       | wjf    |
| 同类型节点特征平均值（`另开一个页面画静态图`）               | txy    |
| 有重边（key>0)的节点的邻居特征值（`另开一个页面画静态图`）   | ldy    |
| 筛选器剩余功能：<br>1. 数字类型节点id筛选【】  <br>2. 邻居节点类型筛选+邻居直连边类型筛选   <br>3. 是否显示邻居之间的连边   <br>4. 出度入度范围筛选 | ll     |
| 数据清洗&理解，id语义相同的节点的连接特征(`等筛选器完了人肉搜索`) |        |
|                                                              |        |



## 6.9

| 进度                                                         | Member  |
| ------------------------------------------------------------ | ------- |
| 知识图谱数据挖掘<br>1. 属性的图结构的网络数据挖掘（18年之后， DL）<br>      半监督，点边的量比较少。但是相关的算法试一试【】 | pny     |
| 有重边（key>0)的节点的邻居特征值<br>8833：company值很大，不跟organization连接 | ldy     |
| 数字类型节点id筛选                                           | ll      |
| 数据清洗&理解，id语义相同的节点的连接特征(`等筛选器完了人肉搜索`) |         |
| 部署了，debug了                                              | yf, wjf |



| ToDo                                                         | Member                                                       | DDL  |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| 知识图谱数据挖掘仓库分头跑<br>【注意：①筛选数据集：3000点，10000边===10000点，10000+边②在共享文档写一点要点(<u>研究方向</u>：点，边，子图；<u>本地跑</u>：四个异常点跟它是否有关系)】<br><br />仓库：[](https://github.com/FelixDJC/Awesome-Graph-Anomaly-Detection)<br />博客：[](https://www.cnblogs.com/pny01/p/17469249.html)<br /> | <u>**仓库**</u>：<br />**1. Traditional Methods()**<br />**2. Deep Methods**<br />【Reconstruction】<br />【Reinforcement Learning】<br />【Generative Adversarial Network】<br />【Filter + One-class SVM + Meta Learning】<br />【Contrastive Learning】<br />【Hybrid Methods】<br />【Other Self-Supervised Learning】<br />【Others】<br />**2. Multi-View Static Graph<br />3. Others**<br /> |      |
| 综述【A Comprehensive Survey on Graph Anomaly Detection with Deep Learning】：[](https://ieeexplore.ieee.org/document/9565320)<br />统计综述【Graph based anomaly detection and description: a survey】[](https://link.springer.com/article/10.1007/s10618-014-0365-y)<br /> | **<u>论文</u>**：<br />                                      |      |
| **同类型节点特征平均值**（`另开一个页面画静态图`）           | pny                                                          |      |
| 筛选器剩余功能：<br>1. 数字类型节点id筛选 【ToDo: 在重复的字符串前加个dup】<br>2. 邻居节点类型筛选+邻居直连边类型筛选 <br>3. 是否显示邻居之间的连边 <br>4. 出度入度范围筛选 | ll                                                           |      |
| 数据清洗&理解，id语义相同的节点的连接特征(`等筛选器完了人肉搜索`) |                                                              |      |
| bfs优化，拍平的数据导入数据库                                |                                                              |      |

**?实际的点和边数量不同**



**开会时间**：晚上九点开始   1个小时   多开



## 6.16

NLP (?)

community detection：networkx 选几种 （modularity, ），结果交集，异常点community分布

层次聚类DBSCAN

数据清洗

根据回答整合的综合界面



## 6.19

1. 对attribute的扩充（Deepwalk etc.)【wjf】

2. PyGOD（留意版本，小样本debug+BOND论文）【ldy】
3. 给受怀疑的四个点(or 排列组合）赋值做**page rank**（u出度5，每条边继承1/5权重），影响大的点值会更大+之前分的【txy】
4. **之前分的** + 系统可视化的设计（读题"Use visual analytics to build a “contextualizer” that provides rich information for the entities listed below"）（关注算法的可解释性）【cl】
5. 数据清洗【pny】
6. community detection算法原理+标注anomaly【yf】



MC2: 链路预测[带时序]

MC3: IUU交易



## 6.21

**进度**：

<u>pagerank大发现！！！！！！！</u>

![](\img\pagerank.jpg)





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

![](\img\LINE.jpg)



**MC1 Questions**：

1. Use visual analytics to <u>dynamically display and explore context around the suspected entities listed above</u>. What did you learn about each one? Can you connect them to illegal fishing? Provide evidence for or against the case that each entity is involved in illegal fishing and use visual analytics to express confidence in your conclusions. Limit your response to 600 words and 6 images.

   【egoNet+（语义信息可视化？把他们跟illegal fishing联系起来？）】

2. Use your <u>visual analytics tool to compare and contrast what you learned about the suspect entities</u>. Are there <u>patterns that may indicate illegal activity</u>? Use visual analytics to express confidence that a pattern exists and where uncertainty may be affecting this confidence. Limit your response to 400 words and 4 images.

   【pagerank 可视化 + attribute平行坐标系 + community detection&聚类】

3. What other companies should FishEye investigate for illegal fishing? Show how your visual analytics can be used to find entities that are worthy of further investigation. Limit your response to 600 words and 6 images.

   【pagerank 可视化 + attribute平行坐标系 + community detection&聚类】

4. Reflection: What was the most difficult aspect of working with this knowledge graph? Did you have the tools and resources you needed to complete the challenge? What additional resources would have helped you? Limit your response to 300 words

   

**ToDo：**

1. **另开一个页面做pagerank可视化筛选器**

   [**拖拽pagerank值过滤显示**其大于某个值的点，观察他们的成环关系和**score流向**]【yf】【txy】【wjf】

2. 调研看看第一问“contextualize”该咋办，怎么把他们跟illegal fishing通过egonet联系起来【ldy】

3. 解决编码问题【cl】



## 6.23



**进展：**

编码：中文双引号

觉得pagerank不完全行，考虑<u>拿出**连通子图**</u>+<u>分出层级结构</u>做分析



同类型多边？

边相似点不相似的模仿行为？

country？



**ToDo:**

1. 以知识图谱为中间产物的NLP调研一下，关注语义（country，movement，location）【ldy】

2. 异常pattern统计：

   <u>入度远大于出度的点的统计，同类型多边套皮的可能 etc.</u>【wjf】

3. 把大图划成子连通分量，之后在异常点所在的连通块上重新**跑之前分的算法**【cl】

4. community detection算法出一个结果和原理分析【yf】

5. 和egonet配套的语义信息卡片【yf, txy, wjf】

6. page rank可视化【-】

7. **跑之前分的算法**，设计UI界面【txy】



<u>**决定**：只做MC1</u>



现有的：【pagerank为主线，其他算法下3388的表现，彼此相连，】



## 6.26

进度：

1. 21个强（任两个点都可达）连通分量：Ocean front自己在一处，其他三个在最大的强连通分量里

2. community detection结果：结果要push一下
3. 知识图谱本身的异常检测，知识补全（算法，模型可以用？）
4. 是否可以验证算法结果

### TO-DO

1. 分离弱连通分量（cl）

2. pagerank在弱连通分量上跑，异常点检测算法是不是也跑一下？

3. 知识图谱的异常检测（群里链接）

   Pattern discovery and anomaly detection via knowledge graph
   https://ieeexplore.ieee.org/abstract/document/8455737 (yf)

   https://juejin.cn/post/7235557683448397880 知识图谱+openAI (wjf)

   https://aclanthology.org/2020.acl-main.412.pdf 知识图谱+QA model (ldy)

   https://zhuanlan.zhihu.com/p/332484010 知识图谱链路预测（边的异常检测）(cl)

   https://zhuanlan.zhihu.com/p/381414265 (txy)

4. 系统的优化（不要分页，不要拖太长，界面的布局更改地更标准）

   1. 边和点的过滤
   2. 在egonet中选中节点展示，其他隐藏（比如隐藏部分目标节点的一阶邻居的一阶邻居）

5. 算法和可视化系统的结合，从可视化系统探索到pattern的方法

6. 算法的结果可以通过计算比例验证？除了点以外是否还需要关注路径和子图

7. 想法：统计三元组 (点A，边，点B）排列组合的类型，看在语义上是否有完全不可理解的或者可以结合IUU理解为异常的关系，进一步通过边的关系定义一定的异常程度，异常边连异常边-->更加可被考虑的异常路径-->尝试找到异常pattern (txy)

8. 更多关于语义的探索 (observation.md大家有没有什么想法)，如何联系IUU




## 6.30

**进度**

1. 系统debug和优化进行中
2. 对语义的探索，手动列表可能不太行
3. IUU定义
4. 论文阅读
5. 比较小的weight边的占比（都是fisheye出来的）

**ToDo**

1. 语义分析调研+实验（第一问），和pny讨论【wjf】
2. 优化系统【yf】
3. 四个可疑点所处连通分量+全图三元组 (点A，边，点B）排列组合的类型统计（同类型连边不同端点排列的占比，同类型端点不同连接的占比，在所有排列组合中的占比等等）【txy】
4. 国家的分布，统计国内&跨国边；统计有哪些（直连国家的个人和公司的数量）小国家处在大的连通分量里【ldy】
5. 四个可疑点环长度的统计+环里可疑点的数目【cl】



## 7.3

目前为止做的事：

1. 系统核心的前端都写了！技术栈没有问题
2. 跑了一些全局检测算法，但是效果不理想，继续**推进**一下在分量里/ego里跑的结果
3. 要从egonet里解释一下IUU可疑之处，正在进行一些统计量的**探索**



**ToDo**

1. 第一问再看看【wjf】+ 分量里/ego里的mat数据，跑强化学习和graph embedding
2. 优化系统（力导向一阶二阶分离，把同类型同方向的边合在一起），优化（现在还没画邻居之间的边）【yf】
3. 四个可疑点所处连通分量+全图三元组 (点A，边，点B）排列组合的类型统计（同类型连边不同端点排列的占比，同类型端点不同连接的占比，在所有排列组合中的占比等等）【txy】
4. 国家的分布，统计国内&跨国边；统计有哪些（直连国家的个人和公司的数量）小国家处在大的连通分量里（准备国家network图的数据[同类型边聚成簇，边权之和代表国家权重]）【ldy】
5. 四个可疑点环长度的统计[以深度提前打断降低复杂度]+环里可疑点的数目【cl】

白天一起干，晚上开小会同步进度

[【知识图谱】Knowledge Graph Embedding: A Survey - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/106024679)

| 日期 | 任务                                          | 人   |
| ---- | --------------------------------------------- | ---- |
| 7.4  | 尝试                                          |      |
| 7.5  | 尝试                                          |      |
| 7.6  | 系统设计+组件实现，不再做别的尝试，开始写解答 |      |
| 7.7  | ——                                            |      |
| 7.8  | ——                                            |      |
| 7.9  | ——                                            |      |
| 7.10 | ——                                            |      |
| 7.11 | ——                                            |      |
| 7.12 | ——                                            |      |
| 7.13 | 中午两点前提交解答                            |      |



## 7.7

<u>Q1</u>

**技术**

1. 资料卡片
2. egonet 优化（hover显示资料卡片，双击切换，单击点亮 ，渲染速度etc.)

**解答**

1. 构建**量化指标**，在图里做验证
2. 组织答案

<u>Q2</u>

