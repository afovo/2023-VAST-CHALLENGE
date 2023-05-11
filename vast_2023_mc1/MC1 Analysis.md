# MC1 Analysis

## Original Question

> Note: This scenario and all the people, places, groups, technologies, contained therein are fictitious. Any resemblance to real people, places, groups, or technologies is purely coincidental.

### Background

Analysts at FishEye International are committed to stopping **illegal**, **unreported**, and **unregulated (IUU) fishing** and **protecting marine species** that are affected by it. As part of their work, FishEye collects online news articles about fishing, marine industry, and international maritime trade. To facilitate their analysis, FishEye uses a natural language processing tool to extract the <u>names of entities (people and businesses) and the relationships between them</u>. The extracted information is transformed into a knowledge graph that analysts would like to use to investigate illegal fishing. One of FishEye’s tasks is investigating tips they receive about possible IUU involvement. To push their investigations forward, FishEye’s analysts need to <u>quickly see, understand, and explore the context around each tip</u>. If they can connect an entity identified in a tip to illegal fishing, they may be able to escalate their investigation. Helpfully, FishEye has included some of their own illegal fishing case studies in the database so the organization and the companies they have investigated appear in the graph.

However, simply showing all information related to a suspected entity will be overwhelming, especially when using a traditional node-link visualization to see context around neighboring entities. Your task is to use visual analytics to help FishEye analysts see, interact with, and understand the context around a tip. Special emphasis should be placed on displaying relevant contextual information and hiding information that is not interesting or relevant. Ideally, the display will be dynamic and interactive. Using visual analytics, can you help FishEye identify companies that could be engaged in illegal fishing?

### Tasks and Questions:

Use visual analytics to build a “contextualizer” that provides **rich information for the entities listed below**. Each entity was identified in a tip received by FishEye, but <u>not all will end up with a substantive connection to illegal fishing</u>. The visualizations you develop should allow analysts to <u>extend the information they see as new entities are discovered</u>.

**Entities to investigate**

1. Mar de la Vida OJSC

   ```json
   {"dataset": "MC1", "id": "Mar de la Vida OJSC"}
   ```

2. 979893388

   ```json
   {"type": "organization", "dataset": "MC1", "id": 979893388}
   ```

3. Oceanfront Oasis Inc Carrie

   ```json
   {"dataset": "MC1", "id": "Oceanfront Oasis Inc Carriers"}
   ```

4. 8327

   ```json
   {"type": "organization", "dataset": "MC1", "id": 8327}
   ```

**Questions**

1. Use <u>visual analytics to dynamically display and explore context around the suspected entities listed above</u>. What did you learn about each one? Can you connect them to illegal fishing? Provide evidence for or against the case that each entity is involved in illegal fishing and use visual analytics to express confidence in your conclusions. Limit your response to 600 words and 6 images.
2. Use your visual analytics tool to compare and contrast what you learned about the suspect entities. Are there <u>patterns that may indicate illegal activity</u>? Use visual analytics to express confidence that a pattern exists and where uncertainty may be affecting this confidence. Limit your response to 400 words and 4 images.
3. What <u>other companies</u> should FishEye investigate for illegal fishing? Show how your visual analytics can be used to find entities that are worthy of further investigation. Limit your response to 600 words and 6 images.
4. Reflection: What was the most difficult aspect of working with this knowledge graph? Did you have the <u>tools and resources you needed to complete the challenge</u>? What additional resources would have helped you? Limit your response to 300 words

> Note: Participants in MC1 should use only data from MC1 for their submissions. Use of external data, including from other mini-challenges or external sources, is discouraged. Participants interested in combining data from other challenges are encouraged to participate in the Grand Challenge.



## Data Notes

KG, directed multi-graph

3721 nodes

7422 edges

json format, supporting <u>d3's node-link format</u> and  <u>networkx</u>.node_link_graph

At the root-level, it is a dictionary with graph-level properties specified as keys ( directed , mulitgraph , graph). 

**Node Attributes:**

- **Id** – Unique identifier of the node, usually the name of the entity, some numeric
- ***type**—{person, organization, company, political_organization, <u>location</u>, vessel, <u>event</u>, <u>movement</u>}
- ***country**—Country associated with the entity
- **dataset** – ‘MC1’

**Edge Attributes:**  

- **source** – ID of the source node
- **target** – ID of the target node
- **weight**—(0,1)
- ***type** – {membership, partnership, ownership, family_relationship}
- **dataset** – ‘MC1’



## Task

1. 对知识图谱的交互可视化

   - 标注目标entities(写成可扩展接口)
   - 可视化目标entities信息，提供探索交互（how?）

2. 找出目标entities中非法捕鱼活动的pattern

   - 调研：非法渔业的定义？有哪些可能的pattern？有无用关系网络监控的先例？

     - Some links:

       [Understanding Illegal, Unreported, and Unregulated Fishing | NOAA Fisheries](https://www.fisheries.noaa.gov/insight/understanding-illegal-unreported-and-unregulated-fishing)

       [Report on IUU Fishing, Bycatch and Shark Catch | NOAA Fisheries](https://www.fisheries.noaa.gov/international/international-affairs/report-iuu-fishing-bycatch-and-shark-catch)

       [Illegal, Unreported, and Unregulated Fishing Causes and Effects (worldwildlife.org)](https://www.worldwildlife.org/threats/illegal-fishing)

       [Approaches to combatting illegal, unreported and unregulated fishing | Nature Food](https://www.nature.com/articles/s43016-020-0121-y)

   - 结合调研结果设计并进行pattern提取
   
3. 用patterns匹配其它entities

4. Reflection on other tools needed





- 画一些小图insight
  - 点形状不同，边颜色不同
- 把数据摊平，每个类型，每条边两边的关系都做一个分析



## Time Line

| DDL  | Task                                                         | Member                                       |
| ---- | ------------------------------------------------------------ | -------------------------------------------- |
| 5.18 | 1. MC1,2 netv.js<br>2. hierarchical-edge-bundling知识图谱可视化，目标实体标注<br>3. 小图分开画，各维度数据分析<br>4. 调研 (知识图谱分析的先例，非法渔业指标，图数据挖掘) | 1. yf<br>2. wjf, txy<br>3. pny<br>4. ldy, ll |
| 5.25 | 1.                                                           |                                              |
|      |                                                              |                                              |
|      |                                                              |                                              |

