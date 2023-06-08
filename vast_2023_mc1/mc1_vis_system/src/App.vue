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
      <!--  邻居节点的类型  -->
      <BarChart :title="'Neighbour Types'" :raw-data="node_type_data"></BarChart>
      <!--      直连边，贡献的出入度，对面点的类型-->
      <StackedColumnChart
          style="width: 1000px; height: 500px"
          :in-data="in_data"
          :out-data="out_data"
      ></StackedColumnChart>
      <!--   邻居之间边的类型   -->
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
import * as d3 from 'd3';

let activeNames = $ref(["Filter", "EgoNet", "BarChart", "StackedColumnChart"]);
let suspicious = new Set([
  "Mar de la Vida OJSC",
  979893388,
  "Oceanfront Oasis Inc Carriers",
  8327,
]);
let unmodified_id = new Set(["23", "38", "626", "621", "77", "90", "16", "98", "93", "96"]);

//接收filter传值
let select_id, show1, show2;

//过滤后的nodes和links
let filter_nodes = $ref(new Set()), filter_links = $ref(new Set())

//统计量寄
let node_type_data = $ref([])
let direct_neighbor_edge;
let n_level
let in_data = $ref(createEmptyMap());
let out_data = $ref(createEmptyMap());

//点击提交按钮后触发
const submit = (filter) => {
  select_id = filter.select_id;
  show1 = filter.show1;
  show2 = filter.show2;

  filter_nodes = new Set();
  filter_links = new Set();
  node_type_data = [];
  direct_neighbor_edge = new Map();
  n_level = [];
  in_data = createEmptyMap();
  out_data = createEmptyMap();

  dfs(select_id, show2 ? 2 : 1)
  getNeighbourType()
  getNeighborConnection(n_level)
  directEdgeStatistic(select_id)
}

/////////ToDo: 数据预处理 存到本地
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
////////数据预处理end///////////////////

// 对纯数字id进行转换
function id_translation(id) {
  if (typeof (id) == "string" && !isNaN(id))
    if (id.charAt(0) !== "0" && !unmodified_id.has(id))   // 待处理的node单独拿出来了 // 如果字符串为纯数字且开头不为0（有个“07”），转格式
      id = parseInt(id)
  return id
}

//dfs过滤目标节点ego_data
//并且把 n level neighbor存起来
function dfs(id, depth) {
  id = id_translation(id)
  let n = nodes.get(id)
  if (!filter_nodes.has(n)) {//如果当前节点没被添加过
    filter_nodes.add(n)

    if (depth === 0) {//到达叶子节点
      n_level.push(id);
      return;
    }
    if (graph.has(id)) {//出度
      graph.get(id).forEach(function (to) {
        // ToDo: depth=1的时候第一次做dfs的时候n_level一定还是空的?
        links[[id, to]].forEach((link)=>{
          filter_links.add(link)
        })
        dfs(to, depth - 1);
      })
    }
    if (rgraph.has(id)) {//入度
      rgraph.get(id).forEach(function (from) {
        links[[from, id]].forEach((link)=>{
          filter_links.add(link)
        })
        dfs(from, depth - 1);
      })
    }
  }
}


///////////////邻居的类型（直方图）/////////////////
function getNeighbourType() {
  let map = new Map()
  filter_nodes.forEach((value) => {
    const count = map.get(value.type!=null?value.type:"undefined") || 0;
    map.set(value.type!=null?value.type:"undefined", count + 1);
  });
  node_type_data = Array.from(map.entries(), ([name, value]) => ({ name, value }));
  node_type_data.sort(function (a, b) {
    if (a.name < b.name) {return -1;}
    if (a.name > b.name) {return 1;}
    return 0;
  });
}

///////////////邻居之间连边的类型数量（直方图）////////
function getNeighborConnection(n_lev_nodes) {
  n_lev_nodes.forEach(ele => {
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


////////////////和目标点直接相连的边的类型（数量+另外一个点的类型）//////////////////
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
  id = id_translation(id)
  if (graph.has(id)) {//出度
    graph.get(id).forEach(function (to) {
          for (let i = 0; i < links[[id, to]].length; i++) {
            let link = links[[id, to]][i]
            let type = link.type == null ? "undefined" : link.type
            let to_type = nodes.get(to).type == null ? "undefined" : nodes.get(to).type
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
}


</script>
