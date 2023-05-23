<template>
  <p>filter: {{select_id}}</p>
  <el-collapse v-model="activeNames">
    <!-- filter -->
    <el-collapse-item title="Filter" name="Filter">
      <Filter @submit="submit"/>
    </el-collapse-item>
    <!-- ego net demo -->
    <el-collapse-item title="EgoNet" name="EgoNet">
      <EgoNet :nodes-raw-data="filter_nodes" :links-raw-data="filter_links"/>
    </el-collapse-item>
  </el-collapse>
</template>
<style scoped></style>
<script setup>
import EgoNet from "./components/ego.vue";
import Filter from "./components/filter.vue";
import {ref} from 'vue';
import * as d3 from 'd3';

let activeNames = $ref(["Filter", "EgoNet"]);

//接收filter传值
let select_id, show1, show2;
let filter_nodes = ref([]), filter_links = ref([])
let duplicate = new Map()
const submit=(filter)=>{
  console.log(filter);
  select_id = filter.select_id;
  show1 = filter.show1;
  show2 = filter.show2;
  filter_nodes.value = [];
  filter_links.value = [];
  duplicate.clear();
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
  console.log(filter_nodes.value)
  console.log(filter_links.value)
}

//过滤目标节点
let nodes = {}
let links = {}
let graph = {}
let rgraph = {}
d3.json("/MC1.json").then(function (raw_data) {
  nodes = raw_data.nodes;
  // for (let i = 0; i < raw_data.nodes.length; i++) {
  //   nodes[raw_data.nodes[i].id] = raw_data.nodes[i]
  // }
  for (let i = 0; i < raw_data.links.length; i++) {
    let link = raw_data.links[i]

    if ([link.source, link.target] in links) {
      links[[link.source, link.target]].push(link)
    } else {
      links[[link.source, link.target]] = [link]
    }

    if (link.source in graph) {
      graph[link.source].push(link.target)
    } else {
      graph[link.source] = [link.target]
    }

    if (link.target in rgraph) {
      rgraph[link.target].push(link.source)
    } else {
      rgraph[link.target] = [link.source]
    }
  }
  console.log('nodes: ')
  console.log(nodes)
  console.log('links: ')
  console.log(links)
  console.log('graph: ' )
  console.log(graph)
});

function dfs(id, depth) {
  if (duplicate.get(id) == null) {
    filter_nodes.value.push(nodes.filter((d)=>d.id === id)[0])
    duplicate.set(id,1)
  }
  if (depth === 0) {
    return;
  }
  if (id in graph) {
    graph[id].forEach(function (to){
      filter_links.value = filter_links.value.concat(links[[id, to]])
      dfs(to, depth-1);
    })
  }
  if (id in rgraph) {
    rgraph[id].forEach(function (from){
      filter_links.value = filter_links.value.concat(links[[from, id]])
      dfs(from, depth-1);
    })
  }
}
</script>
