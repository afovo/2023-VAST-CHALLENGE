<template>
  <div id="main" style="border: solid"></div>
</template>

<style scoped>
#main {
  width: 80%;
  margin-left: 10%;
  margin-right: 10%;
  height: 90vh;
  margin-top: 3vh;
  margin-bottom: 3vh;
}
</style>
<script setup>
import NetV from "netv";
import * as d3 from "d3";
let data = $ref({ nodes: [], links: [] });
let min = $ref(3);
let max = $ref(400);

// 读取json，存入nodes和links数据
const init_data = function () {
  let nodes, links, from, to, source, target;
  let node_degree = {};
  let id, idSet, link_map, reverse_from;
  d3.json("/MC1.json").then(function (raw_data) {
    nodes = raw_data.nodes;
    links = raw_data.links;
    // 统计每个节点的出入度
    links.forEach((e) => {
      from = e.source.toString();
      to = e.target.toString();
      from in node_degree
        ? node_degree[from].out_degree++
        : ((node_degree[from] = {}),
          (node_degree[from].out_degree = node_degree[from].in_degree = 0));
      to in node_degree
        ? node_degree[to].in_degree++
        : ((node_degree[to] = {}),
          (node_degree[to].out_degree = node_degree[to].in_degree = 0));
    });
    // 统计最大出入度
    var in_d = (d) => {
      return d.in_degree;
    };
    var out_d = (d) => {
      return d.out_degree;
    };

    var arr = Object.values(node_degree);
    // console.log("out: " + d3.extent(arr, out_d));
    // console.log("in: " + d3.extent(arr, in_d));

    // 遍历原始nodes,去重,并根据出度,筛选需要的节点
    idSet = new Set();
    nodes.forEach((node) => {
      id = node.id.toString();
      // 第一个加入，后续重复的不管
      if (!idSet.has(id)) {
        if (id in node_degree) {
          var out_d = node_degree[id].out_degree;
          if (min <= out_d && out_d <= max) {
            data.nodes.push({ id: id });
            idSet.add(id);
          }
        }
      }
    });
    // TODO: links 也需要去重
    link_map = {};
    links.forEach((link) => {
      from = link.source.toString();
      to = link.target.toString();
      link_map[from] = to;
    });
    Object.keys(link_map).forEach((from) => {
      source = from;
      target = link_map[from];
      if (
        source != link_map[target] &&
        idSet.has(source) &&
        idSet.has(target)
      ) {
        id = source + "=>" + target;
        data.links.push({ id: id, source: source, target: target });
      }
    });
    // view data
    // console.log(max_out_degree, max_in_degree);
  });
};
const init_net = function () {
  const div = document.getElementById("main");
  const width = div.clientWidth;
  const height = div.clientHeight;

  const colorScale = null;

  const netV = new NetV({
    container: div,
    width: width,
    height: height,
    node: {
      style: {
        r: 8,
      },
    },
    link: {
      style: {
        strokeWidth: 1,
      },
    },
  });
  data.nodes.forEach((node) => {
    // NOTE: build-in dataset contains position, random it
    node.x = Math.random() * 500 + 150; // scale and offset to center
    node.y = Math.random() * 500;
    node.color = "#fff";
  });
  netV.data(data);

  netV.on("zoom", () => {});
  netV.on("pan", () => {});

  const simulation = d3
    .forceSimulation(data.nodes)
    .force(
      "link",
      d3.forceLink(data.links).id((d) => d.id)
    )
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));

  simulation.on("tick", () => {
    data.nodes.forEach((n) => {
      const node = netV.getNodeById(n.id);
      node.x(n.x);
      node.y(n.y);
    });

    netV.draw();
  });
};

setTimeout(init_data, 1);
setTimeout(init_net, 500);
</script>
