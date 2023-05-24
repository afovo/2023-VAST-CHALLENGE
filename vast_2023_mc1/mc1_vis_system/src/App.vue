<template>
  <el-collapse v-model="activeNames">
    <!-- filter -->
    <el-collapse-item title="Filter" name="Filter">
      <Filter @submit="submit"/>
    </el-collapse-item>
    <!-- ego net -->
    <el-collapse-item title="EgoNet" name="EgoNet">
      <EgoNet :nodes-raw-data="filter_nodes" :links-raw-data="filter_links"/>
    </el-collapse-item>
    <!--  Analysis Charts  -->
    <el-collapse-item title="Analysis" name="Analysis">
      <BarChart :title="'Neighbour Types'" :raw-data="node_type_data"></BarChart>
<!--      <BarChart :title="'Edge Types'" :raw-data="x"></BarChart>-->
    </el-collapse-item>
  </el-collapse>
</template>
<style scoped></style>
<script setup>
import EgoNet from "./components/ego.vue";
import Filter from "./components/filter.vue";
import BarChart from "./components/charts/BarChart.vue";
import {ref} from 'vue';
import * as d3 from 'd3';

let activeNames = $ref(["Filter", "EgoNet", "BarChart"]);

//接收filter传值
let select_id, show1, show2;
let filter_nodes = ref([]), filter_links = ref([])
let node_type_data = new Map()
let x;

let node_type_map = new Map()//id=>type 用来做邻居类型统计&节点去重
const submit=(filter)=>{
  select_id = filter.select_id;
  show1 = filter.show1;
  show2 = filter.show2;

  filter_nodes.value = [];
  filter_links.value = [];
  node_type_data = new Map();
  node_type_map = new Map();

  //test
//   filter_nodes.value = [{dataset: 'MC1', id: 'Oceanfront Oasis Inc Carriers'},{type: 'organization', dataset: 'MC1', id: 2262},
//   {type: 'organization', dataset: 'MC1', id: 8787}, {type: 'organization', dataset: 'MC1', id: 979893388},{type: 'organization', dataset: 'MC1', id: 'FishEye International'}]
//   filter_links.value = [
//
//     {
//       "type": "ownership",
//       "weight": 0.8363937,
//       "dataset": "MC1",
//       "source": 979893388,
//       "target": "Oceanfront Oasis Inc Carriers",
//       "key": 0
//     },
//     {
//       "type": "membership",
//       "weight": 0.4461,
//       "dataset": "MC1",
//       "source": "FishEye International",
//       "target": "Oceanfront Oasis Inc Carriers",
//       "key": 0
//     },
//     {
//       "type": "family_relationship",
//       "weight": 0.8220089,
//       "dataset": "MC1",
//       "source": 8787,
//       "target": "Oceanfront Oasis Inc Carriers",
//       "key": 0
//     },
//     {
//       "type": "family_relationship",
//       "weight": 0.83553725,
//       "dataset": "MC1",
//       "source": 2262,
//       "target": "Oceanfront Oasis Inc Carriers",
//       "key": 0
//     }
// ]
  dfs(select_id, show2?2:1)
  console.log(filter_nodes)
  console.log(filter_links)
  statistic()
  x=[{name:'a',value:1}]
}

//数据预处理
let nodes = new Map()//id=>node对象
let links = {}//[source_id, target_id]=>[link对象1, link对象1...]
let graph = new Map()//id=>[出边指向的邻居节点id1, id2...]
let rgraph = new Map()//id=>[入边指向的邻居节点id1, id2...]
d3.json("/MC1.json").then(function (raw_data) {
  //ToDo:需要测试‘1’和1作为key值可以用map存吗？或者字典用[]取值是不是有问题？
  for (let i = 0; i < raw_data.nodes.length; i++) {
    nodes.set(raw_data.nodes[i].id,raw_data.nodes[i]);
  }
  for (let i = 0; i < raw_data.links.length; i++) {
    let link = raw_data.links[i]

    if ([link.source, link.target] in links) {
      links[[link.source, link.target]].push(link)
    } else {
      links[[link.source, link.target]] = [link]
    }
    // if (links.has({s:link.source, t:link.target})) {
    //   let arr = links.get({s:link.source, t:link.target})
    //   arr.push(link)
    //   links.set({s:link.source, t:link.target}, arr)
    //   // console.log(links.get([link.source, link.target]))
    // } else {
    //   links.set({s:'shit'},'fuck')
    //   console.log(links.get({s:'shit'}))
    // }

    if (graph.has(link.source)) {
      let arr = graph.get(link.source)
      arr.push(link.target)
      graph.set(link.source, arr)
    } else {
      graph.set(link.source,[link.target])
    }

    if (rgraph.has(link.target)) {
      let arr = rgraph.get(link.target)
      arr.push(link.source)
      rgraph.set(link.target, arr)
    } else {
      rgraph.set(link.target, [link.source])
    }
  }
  console.log('nodes: ')
  console.log(nodes)
  console.log('links: ')
  console.log(links)
  console.log('graph: ' )
  console.log(graph)
});

//过滤目标节点ego_data
function dfs(id, depth) {
  if (node_type_map.get(id) == null) {//如果当前节点没被添加过
    let n = nodes.get(id)
    filter_nodes.value.push(n)
    node_type_map.set(id, n.type==null?"undefined":n.type)
    if (depth === 0) {//到达叶子节点
      return;
    }
    if (graph.has(id)) {//出度
      graph.get(id).forEach(function (to){
        console.log(links[[id, to]])
        filter_links.value = filter_links.value.concat(links[[id, to]])
        dfs(to, depth-1);
      })
    }
    if (rgraph.has(id)) {//入度
      rgraph.get(id).forEach(function (from){
        filter_links.value = filter_links.value.concat(links[[from, id]])
        dfs(from, depth-1);
      })
    }
  }
}

//统计量处理【可以在dfs里加东西】
function statistic(){
  ///////////////邻居的类型（直方图）/////////////////
  let keys = Array.from(node_type_map.keys())
  let values = Array.from(node_type_map.values())
  for (let i = 0; i<keys.length; i++){
    let cnt = node_type_data.get(values[i])
    if (cnt != null) {
      node_type_data.set(values[i], cnt+1)
    } else {
      node_type_data.set(values[i], 1)
    }
  }
  keys = Array.from(node_type_data.keys())
  values = Array.from(node_type_data.values())

  node_type_data = []
  for (let i = 0; i<keys.length; i++){
    node_type_data.push({name:keys[i], value: values[i]})
  }
  node_type_data.sort(function (a, b) {
    if (a.name < b.name) {
      return -1;
    }
    if (a.name > b.name) {
      return 1;
    }
    return 0;
  });

  //ToDo:目标点的出入度
  //ToDo:和目标点直接相连的边的类型（数量+另外一个点的类型）
  //ToDo:一阶邻居之间连边的类型数量（直方图）
}
///////////////////////////////////////////////



</script>
