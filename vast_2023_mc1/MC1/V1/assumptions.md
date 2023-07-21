png xi  Line

1. 和979893388直连 (family&member)，是他的国家Country_628643中唯一的成员

country内的人拥有的组织要不要算做是这个country的东西，但也有可能多个country的人共同拥有

反过来想：979893388直连的点中是他们国家唯一的成员的情况：

![image-20230704175602216](/Users/knovvx/Library/Application Support/typora-user-images/image-20230704175602216.png)

只有'png xi  Line', 'Mar del Oeste Pic', 并且这两个都是十分大的公司，和别的国家往来特别多，并且mar拥有png

但确实国家内只有一个成员的话就不会有国内的交易了

他们共同的owner:['41398ea8-d14a-4666-80e8-6a212684d871',location,connect to 他俩和一个双向拥有的undefine,undefine直连3388

 '903311212', big org, connect to 3388(fam+mem)

'cd7cb49f-0021-4fe9-a3a9-cc8b3fce0c57', 只拥有他俩的location

'SeaSpray Wave SRL Solutions', big undefined, connect to 3388(fam+mem)

 'Ocean Fisheries Llc'] big undefined, connect to 3388(fam+own)

意思是可疑点A连接小国B，A和B的关系与A和B的owner的关系类型一致？

看一下其他连接只有一个国家的点

![image-20230704203634203](/Users/knovvx/Library/Application Support/typora-user-images/image-20230704203634203.png)

['41398ea8-d14a-4666-80e8-6a212684d871',location,connect to 他俩和一个双向拥有的undefine,undefine不连他

 '903311212',connect to 185040354,mem

'cd7cb49f-0021-4fe9-a3a9-cc8b3fce0c57', 只拥有他俩的location

'SeaSpray Wave SRL Solutions', big undefined, 不连他

 'Ocean Fisheries Llc'] big undefined, 不连他







其他3个可疑点没有和只有一个成员的国家的出边

![image-20230704192312262](/Users/knovvx/Library/Application Support/typora-user-images/image-20230704192312262.png)

一直到10个成员以下的国家，都只有mar de la出现了，是两个人属于Polarisdom，一共有4个成员，3个人1个公司，2个人和mar直连，1个公司是mar的二阶邻居并且只有一条边，是出边指向mar的一阶邻居，剩下一个人是孤立的，和一个location自成一个连通分量

作为参考的所有国家数量：但是确实和这三个可疑点直连的人和公司本来就少

![image-20230704192629370](/Users/knovvx/Library/Application Support/typora-user-images/image-20230704192629370.png)



## 船溯源

关于船：115艘，30艘有指入的ownership，15艘可以沿着ownership的链条找到有国家的company或人，但有一对多的情况，15艘会断掉，就是找到某个unknown的source之后不再有指入。

**可以找到的15艘：**

**'19', 'USCGC', 'shrimper', 'USCGâ\x80\x99s', 'CutterOliverHenry', 'bottom', 'Rapido beam trawler', 'ocean', 'Kenworth 18-wheeler', 'cutters', 'Leng 999 Gal', 'Ships', 'Oliver', 'salmon', 'Cutters'**

没找到的15艘:

'Craftâ\x80\x93Law', 'Tian', 'Cutter', 'HMS Montrose', 'USCGC Spencer', 'WMEC', **'water**', 'Fu Yuan Yu Leng 999', '**ARA Contraalmirante Cordero**', 'DDG', 'Gulf', 'dup18', 'wheeler', 'Wartsila', 'PC'

黑的俩分别和8327和3388相连

85艘没有指入的ownership的船 和可疑点的情况：只有8327和Coast相连, 这艘船拥有8327,并且他没有入度，还拥有Cutter,cutters,Craftâ\x80\x93Law，其中两艘都没有国籍，Cutter通过两层organization可以找到两个人拥有这个organization. 

person--> 55674-->21538->Cutter

____

### 船与可疑点

**115艘里面3（没有国家）+1（可以找到国家的）艘直连可疑点，9艘连不到可疑点(不在一个弱连通）**

**106艘和可疑点在同一个弱连通分量**

**19艘在强连通分量里，3艘不在强连通：Tian dup18 AirPods, 其他应该是单向指向或被指入强连通分量中的节点**

Tian和dup18互相拥有，dup18拥有png xi  Line，可以单向到3388

Airpods和未知的6 Ray LLC Enterprises互为partnership，这个未知拥有SeaSpray Wave SRL Solutions，seaspray可以和3388双向抵达

### 强连通19艘

'dup77', 'water', 'Gulf', 'salmon', 'Plastic', '19', 'dup626', '629', 'ocean', 'bottom', 'USS', 'PC', **'Oliver'**, 'HMS Montrose', 'Talleyâ\x80\x99s', 'Ships', 'trucking', 'Deepwater Horizon', 'Vessels'

USS拥有Gulf拥有HMS Montrose，并且Gulf拥有Ocean Fisheries Llc 

Dup77,ocean,629周围看起来很多多边形

19和PC周围都有Faroe的多边形环，但是多边形顶点不太一样





#### 直连4艘

所有船里和可疑点直连的关系: 粗体是可以通过ownership溯源的

8327有3艘：water，**cutters**，Coast（从下到上)

435054320(org)+40213337(org)+movement(weeks)+cutters+Coast每两个物体之间都有连边

都是membership和ownership，很像有规律的渔船活动

cutters有国家，通过Mar del Oeste Pic到40213337到他

![image-20230708104249801](/Users/knovvx/Library/Application Support/typora-user-images/image-20230708104249801.png)

3388有一艘：ARA Contraalmirante Cordero（被7548555拥有，被3388指入membership）

#### 连不到的

106/115艘在最大的弱连通分量里，还有9艘是连不到可疑点的

9艘：USCGC Spencer, WMEC, Deckhands, **USCGâs, CutterOliverHenry**,Spaceflight, HawkEye, reefer, Fu Yuan Yu Leng 999

left: Cutter(red)+USCGâs,        center:HawkEye     right: 这两艘只有一条关系

<center class="half"> 
  <img src="/Users/knovvx/Library/Application Support/typora-user-images/image-20230708102304877.png" width="200"/> 
  <img src="/Users/knovvx/Library/Application Support/typora-user-images/image-20230708102535825.png" width="200"/> 
  <img src="/Users/knovvx/Library/Application Support/typora-user-images/image-20230708102857688.png" width="200"/>
</center>

wmec+uscgc Spencer , spaceflight, deckhands

<center class="half"> 
  <img src="/Users/knovvx/Desktop/截屏2023-07-08 10.32.36.png" width="200"/> 
  <img src="/Users/knovvx/Library/Application Support/typora-user-images/image-20230708103457670.png" width="200"/> 
  <img src="/Users/knovvx/Library/Application Support/typora-user-images/image-20230708103536314.png" width="200"/>
</center>



