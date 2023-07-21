### Relationship

### 调研方面

semantic communication相关？

好像是可以从KG中extract semantic information的方法，但好像没有看到代码，还没仔细看

https://arxiv.org/abs/2202.11958

Google Research 开发的T5模型: Text-To-Text Transfer Transformer model

https://github.com/google-research/text-to-text-transfer-transformer

___

### 一些观察

容器，出入相连的树状 逐步探索 **都在大连通分量**里看?

1. FishEye 直接和oceanfront以及mar de la相连，4个可疑点相连的顺序：

   ​	8327 --> calvin salas -->b856--xx -->Mar de la

   ​                                                           |<--3388-->Ocean 

2. FishEye直连全是membership，除了903311212是ownership

3. 在只有**出度**的点里，包括FishEye一共有32个点直接和可疑点相连，只有入度的点里一共有30个直接和可疑点相连。

4. decfc924-5bdc-4fba-8bbd-bb57d8d478d9只有出度并且直接和可疑点相连，decfc924-5bdc-4fba-8bbd-bb57d8d478d9一阶邻居只有mar de la和KevinBurnett（人）并且这个人和mar de la 是双向的partnership

5. 所有人和公司都有国家，一共只有90个company，1000+人，是不是专门可以看一下人的统计量，然后一些只有关系简单的就筛掉了。

6. 画一下country分布，看一下跨国情况? country需要编码进egonet里去吗

9. Rio Solovia，整个国家只有2人，且是family关系，且没有与任何其他的东西产生联系
10. Family 和owner可不可以单独画一下看能不能有层级划分：好像很困难稍微看了一下感觉会有环并且很零散（family）
11. Vessel, person, location的link也可以单独看一下
12. 从**仅出** 到 **仅入**找path：先看involve了可疑点的
13. 可疑点间互相抵达的路径
14. 看了一下国家间的link关系，注意看了一下只直接流出到一个国家的和只有一个国家流入的。。。。流出的基本上就是断开的family关系，6个里有4个间接关系比较复杂: jeremy, zachary,_ ,_但是他只流向一个国家是因为本身该节点的person联系就非常少

15. weight应该也是为networkx格式提供的？不知道权重具体的含义。

____

### 系统方面

1. 每个边和点类型的filter感觉还是有必要enable的?
2. 能不能enable在邻居中选中筛选，这样可以不看一些特别大的已知的组织的邻居更好观察细节
3. 可以加一个搜索的框？就是相当于像我们直接在MC1的json里搜索的结果一样，感觉有点用（？）



mar de la: 海洋的（hhh西语

movement可不可以暂且理解成在name处产生的move？(...好像还是很奇怪)

political有什么重要角色和理解吗，把它单独于organization作为一个type

person有国家，person有vessel，company有国家，company和人和船可能有雇佣关系，但是A国家的公司雇B国家的人用他的船也 情有可原吗

公司或组织和人没关系但是用了他的船，这种会有问题吗

。。好混乱的瞎猜