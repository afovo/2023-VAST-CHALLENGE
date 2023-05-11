# MC2 Analysis

## Original Question

The country of Oceanus has sought FishEye International’s help in identifying companies possibly engaged in **illegal, unreported, and unregulated (IUU) fishing**. As part of the collaboration, FishEye’s analysts received <u>import/export data for Oceanus’ marine and fishing industries</u>. However, Oceanus has informed FishEye that the <u>data is incomplete</u>. To facilitate their analysis, FishEye transformed the trade data into a <u>knowledge graph</u>. Using this knowledge graph, they hope to understand business relationships, including finding links that will help them stop IUU fishing and protect marine species that are affected by it. FishEye analysts found that node-link diagrams gave them a good high-level overview of the knowledge graph. However, they are now **looking for visualizations that provide more detail about patterns for entities in the knowledge graph**. There are two main parts to this analysis.

First, FishEye knows from past experience that **companies caught fishing illegally will shut down but will then often start up again under a different name**. FishEye wants your help to <u>visualize temporal patterns</u> so they can compare the activities of companies over time to determine if the companies have returned to their nefarious acts.

Second, FishEye has been using several tools, including artificial intelligence, to reason on the knowledge graph and suggest links that could extend the dataset. They have <u>supplied 12 groups of link suggestions</u> and need your help evaluating these groups to identify **which tools are most reliable for completing the graph**. FishEye is especially interested in identifying new temporal patterns or anomalies that are only present when new links are added.

Using visual analytics, can you help FishEye identify companies that may be engaged in illegal fishing?

### Tasks and Questions:

1. Use visual analytics to <u>identify temporal patterns for individual entities and between entities</u> in the knowledge graph FishEye created from trade records. Categorize the types of business relationship patterns you find. Limit your response to 600 words and 6 images.
2. Evaluate the sets of <u>predicted knowledge graph links</u> FishEye has provided using visual analytics. Which sets are most <u>reliable</u> for completing the graph? Limit your response to 600 words and 6 images.
3. Illustrate how your visual analytics approach can be used to <u>identify new patterns and/or anomalies</u> that are present in the knowledge graph after you have added the links you deemed reliable in question 2. Limit your response to 300 words and 4 images.
4. <u>Identify companies that fit a pattern of illegal fishing</u>. Use visualizations to support your conclusions and your confidence in them. Limit your response to 300 words and 4 images.
5. Reflection: What was the most difficult aspect of working with this knowledge graph? Did you have the <u>tools and resources</u> you needed to complete the challenge? What additional resources would have helped you? Limit your response to 300 words

> Note: Participants in MC2 should use only data from MC2 for their submissions. Use of external data, including from other mini-challenges or external sources, is discouraged. Participants interested in combining data from other challenges are encouraged to participate in the Grand Challenge.



## Task

1. 对知识图谱的交互可视化
2. 评估各个预测图谱的可靠性（how？）
3. 找出各entities及其互相贸易的长期pattern
4. 找出有非法捕鱼pattern的公司



## Data Note

### **Main Graph:** 

KG, directed multi-graph

34552 nodes

5464092 directed edges (from shipper to receiver) 

json format, supporting <u>d3's node-link format</u> and  <u>networkx</u>.node_link_graph



At the root-level, it is a dictionary with graph-level properties specified as keys ( directed , mulitgraph , graph). 

```
{'directed': True,

 'mulitgraph': True,

 'graph': {},

 'nodes': [{'id': 1, 'dataset': 'MC2'},

 {'id': 2, 'dataset': 'MC2'}],

 'links': [{'source': 1,

 'target': 2,

 'datset': 'MC2'}] 

}
```

**Node Attributes:** 

- **id** -- Name or numerical number of the company that originated (or received) the shipment 
- **shpcountry** -- Country the company most often associated with when shipping 
- **rcvcountry** -- Country the company most often associated with when receiving 
- **dataset** -- 'MC2' 

**Edge Attributes:** 

- **arrivaldate** -- Date the shipment arrived at port in YYYY-MM-DD format. 
- **hscode** -- Harmonized System code for the shipment. Can be joined with the **hscodes table（？）** to get additional details. 
- **valueofgoods_omu** -- Customs-declared value of the total shipment, in Oceanus Monetary Units (OMU) 
- **volumeteu** -- The volume of the shipment in 'Twenty-foot equivalent units', roughly how many 20-foot standard containers would be required. (Actual number of containers may have been different as there are 20ft and 40ft standard containers and tankers that do not use containers) 
- **weightkg** -- The weight of the shipment in kilograms (if known) 
- **dataset** -- 'MC2' 
- **type** -- 'shipment'
- **generated_by** -- Name of the program that generated the edge. (Only found on 'bundle' records.) 



### Bundles 

Each bundle represents the output of an AI program for link inference. Each bundle represents a list of potential edges to add to the main graph. The challenge is to decide **WHICH of these bundles should be used** (and present evidence for why the selected bundles should be used). 

The bundles are: 

carp 

catfish 

chub_mackerel 

cod2 

herring 

lichen 

mackerel

pollock 

salmon 

salmon_wgl

shark 

tuna