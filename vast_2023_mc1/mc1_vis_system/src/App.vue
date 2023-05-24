<template>
  <el-collapse v-model="activeNames">
    <!-- filter -->
    <el-collapse-item title="Filter" name="Filter">
      <Filter @submit="submit" />
    </el-collapse-item>
    <!-- ego net -->
    <el-collapse-item title="EgoNet" name="EgoNet">
      <EgoNet :nodes-raw-data="filter_nodes" :links-raw-data="filter_links" />
    </el-collapse-item>
    <!--  Analysis Charts  -->
    <el-collapse-item title="Analysis" name="Analysis">
      <BarChart :title="'Neighbour Types'" :raw-data="node_type_data"></BarChart>
      <!--      <BarChart :title="'Edge Types'" :raw-data="x"></BarChart>-->
      <StackedColumnChart
          style="width: 800px; height: 500px"
          :in-data="in_data"
          :out-data="out_data"
      ></StackedColumnChart>
      <BarChart :title="'Edge Types'" :raw-data="direct_neighbor_edge"></BarChart>
    </el-collapse-item>
  </el-collapse>
</template>
<style scoped></style>
<script setup>
import EgoNet from "./components/ego.vue";
import Filter from "./components/filter.vue";
import BarChart from "./components/charts/BarChart.vue";
import StackedColumnChart from "./components/charts/StackedColumnChart.vue";
import {ref} from 'vue';
import * as d3 from 'd3';

let activeNames = $ref(["Filter", "EgoNet", "BarChart", "StackedColumnChart"]);
let suspicious = new Set([
  "Mar de la Vida OJSC",
  979893388,
  "Oceanfront Oasis Inc Carriers",
  8327,
]);


//接收filter传值
let select_id, show1, show2;
let filter_nodes = ref([]), filter_links = ref([])
let node_type_data = new Map()
let direct_neighbor_edge;
let n_level

let node_type_map = new Map()//id=>type 用来做邻居类型统计&节点去重
let in_data = $ref(createEmptyMap());
let out_data = $ref(createEmptyMap());
const submit = (filter) => {
  select_id = filter.select_id;
  show1 = filter.show1;
  show2 = filter.show2;

  filter_nodes.value = [];
  filter_links.value = [];
  node_type_data = new Map();
  node_type_map = new Map();
  direct_neighbor_edge = new Map();
  n_level = [];

  dfs(select_id, show2 ? 2 : 1)
  console.log(filter_nodes)
  console.log("filter_links", filter_links.value.length)
  // console.log(nodes.get(185106))
  console.log("nnnn:", n_level)
  // n_level=n_level.slice(select_id)
  getNeighborConnection(n_level)
  console.log("filter_links ++", filter_links.value.length)
  statistic()
  directEdgeStatistic(select_id)
  x = [{name: 'a', value: 1}]
  // x = [{ name: 'a', value: 1 }]
  console.log("x", direct_neighbor_edge)
}

//数据预处理
let nodes = new Map()//id=>node对象
let links = {}//[source_id, target_id]=>[link对象1, link对象1...]
let graph = new Map()//id=>[出边指向的邻居节点id1, id2...]
let rgraph = new Map()//id=>[入边指向的邻居节点id1, id2...]
d3.json("/MC1.json").then(function (raw_data) {
  for (let i = 0; i < raw_data.nodes.length; i++) {
    if (suspicious.has(raw_data.nodes[i].id))
      raw_data.nodes[i].color = '#FF6374'
    nodes.set(raw_data.nodes[i].id, raw_data.nodes[i]);
  }
  for (let i = 0; i < raw_data.links.length; i++) {
    let link = raw_data.links[i]

    if ([link.source, link.target] in links) {
      links[[link.source, link.target]].push(link)
    } else {
      links[[link.source, link.target]] = [link]
    }

    if (graph.has(link.source)) {
      let arr = graph.get(link.source)
      arr.push(link.target)
      graph.set(link.source, arr)
    } else {
      graph.set(link.source, [link.target])
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
  console.log('graph: ')
  console.log(graph)
});

//过滤目标节点ego_data
// n level neighbor存起来

function dfs(id, depth) {
  if (node_type_map.get(id) == null) {//如果当前节点没被添加过
    let n = nodes.get(id)
    filter_nodes.value.push(n)
    node_type_map.set(id, n.type == null ? "undefined" : n.type)

    if (depth === 0) {
      n_level.push(n['id']);
      //到达叶子节点
      return;
    }
    if (graph.has(id)) {//出度
      graph.get(id).forEach(function (to) {
        console.log(links[[id, to]])
        // depth=1的时候第一次做dfs的时候n_level一定还是空的?

        filter_links.value = filter_links.value.concat(links[[id, to]])
        dfs(to, depth - 1);
      })
    }
    if (rgraph.has(id)) {//入度
      rgraph.get(id).forEach(function (from) {
        filter_links.value = filter_links.value.concat(links[[from, id]])
        dfs(from, depth - 1);
      })
    }
  }
}
function getNeighborConnection(n_lev_nodes) {
  n_lev_nodes.forEach(ele => {
    // console.log("n level elements", ele)
    if (graph.has(ele)) {//出度
      graph.get(ele).forEach(function (to) {

        if (n_lev_nodes.indexOf(to) >= 0) {
          //ToDo:先不画邻居间的边提升一下性能
          // filter_links.value = filter_links.value.concat(links[[ele, to]])
          var type = links[[ele, to]][0].type
          var num = direct_neighbor_edge.get(type)
          if (num != null) {
            // console.log("numm", num)
            direct_neighbor_edge.set(type, num + 1)
          } else {
            direct_neighbor_edge.set(type, 1)
          }
        }
      })
    }
    // if (rgraph.has(ele)) {//入度
    //   rgraph.get(ele).forEach(function (from) {
    //     if (n_lev_nodes.indexOf(from) >= 0) {
    //       filter_links.value = filter_links.value.concat(links[[from, ele]])
    //       var type = links[[from, ele]][0].type+ "_in"
    //       // console.log("ttttt", type)
    //       var num = x.get(type)
    //       if (num != null) {
    //         x.set(type, num + 1)
    //       } else {
    //         x.set(type, 1)
    //       }
    //     }
    //   })
    // }

  })
  var keys = Array.from(direct_neighbor_edge.keys())//edgetypes
  var values = Array.from(direct_neighbor_edge.values())//numbers of each type

  direct_neighbor_edge = []
  for (let i = 0; i < keys.length; i++) {
    direct_neighbor_edge.push({ name: keys[i], value: values[i] })
  }
  direct_neighbor_edge.sort(function (a, b) {
    if (a.name < b.name) {
      return -1;
    }
    if (a.name > b.name) {
      return 1;
    }
    return 0;
  });
}

//统计量处理【可以在dfs里加东西】
function statistic() {
  ///////////////邻居的类型（直方图）/////////////////
  let keys = Array.from(node_type_map.keys()) //node key
  // 把自己的type也算上了？
  let values = Array.from(node_type_map.values()) //node type

  for (let i = 0; i < keys.length; i++) {
    let cnt = node_type_data.get(values[i])
    if (cnt != null) {
      node_type_data.set(values[i], cnt + 1)
    } else {
      node_type_data.set(values[i], 1)
    }
  }


  keys = Array.from(node_type_data.keys())//node types
  values = Array.from(node_type_data.values())//numbers of each type

  node_type_data = []
  for (let i = 0; i < keys.length; i++) {
    node_type_data.push({ name: keys[i], value: values[i] })
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


  //ToDo:一阶邻居之间连边的类型数量（直方图）

}

///////////////////////////////////////////////

//ToDo:和目标点直接相连的边的类型（数量+另外一个点的类型）
function createEmptyMap() {
  return new Map([
    ['person', Array(5).fill(0)],
    ['organization', Array(5).fill(0)],
    ['company', Array(5).fill(0)],
    ['political_organization', Array(5).fill(0)],
    ['location', Array(5).fill(0)],
    ['vessel', Array(5).fill(0)],
    ['movement', Array(5).fill(0)],
    ['event', Array(5).fill(0)],
    ['undefined', Array(5).fill(0)]
  ]);
}

function directEdgeStatistic(id) {
  if (graph.has(id)) {//出度
    graph.get(id).forEach(function (to) {
          for (let i = 0; i < links[[id, to]].length; i++) {
            let link = links[[id, to]][i]
            let type = link.type == null ? "undefined" : link.type
            let to_type = nodes.get(to).type == null ? "undefined" : nodes.get(to).type
            console.log('txy link type')
            console.log(type)
            console.log('txy to type')
            console.log(to_type)
            if (type === 'membership') {
              out_data.get(to_type)[0]++
            } else if (type === 'partnership') {
              out_data.get(to_type)[1]++
            } else if (type === 'ownership') {
              out_data.get(to_type)[2]++
            } else if (type === 'family_relationship') {
              out_data.get(to_type)[3]++
            } else if (type === 'undefined') {
              out_data.get(to_type)[4]++
            }
          }
        }
    )
  }
  if (rgraph.has(id)) {//入度
    rgraph.get(id).forEach(function (from) {
          for (let i = 0; i < links[[from, id]].length; i++) {
            let link = links[[from, id]][i]
            let type = link.type == null ? "undefined" : link.type
            let from_type = nodes.get(from).type == null ? "undefined" : nodes.get(from).type
            console.log('txy link type')
            console.log(type)
            console.log('txy from type')
            console.log(from.type)
            if (type === 'membership') {
              in_data.get(from_type)[0]++
            } else if (type === 'partnership') {
              in_data.get(from_type)[1]++
            } else if (type === 'ownership') {
              in_data.get(from_type)[2]++
            } else if (type === 'family_relationship') {
              in_data.get(from_type)[3]++
            } else if (type === 'undefined') {
              in_data.get(from_type)[4]++
            }
          }
        }
    )
  }
  console.log('txytxytxy outdata')
  console.log(out_data)
  console.log('txytxytxy indata')
  console.log(in_data)
}


</script>
