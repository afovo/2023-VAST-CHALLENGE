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
| 5.25 | 1.                                                           |                                              |
|      |                                                              |                                              |
|      |                                                              |                                              |

