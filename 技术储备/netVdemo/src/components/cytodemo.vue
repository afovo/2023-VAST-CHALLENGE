<template>
  <button id="layoutButton" type="button">CoSE-Bilkent</button>
  <div id="cy"></div>
</template>
<style>
#cy {
  width: 1200px;
  height: 700px;
  display: block;
  border: solid;
  position: absolute;
}
</style>
<script setup>
import cytoscape from "cytoscape";
import coseBilkent from "cytoscape-cose-bilkent";
import * as d3 from "d3";
let data = $ref([
  { data: { id: 1 } },
  { data: { id: 2 } },
  { data: { id: 3 } },
  { data: { id: "1_2", source: 1, target: 2 } },
  { data: { id: "1_3", source: 1, target: 3 } },
  { data: { id: "2_3", source: 2, target: 3 } },
]);
let min = $ref(6);
let max = $ref(7);
// 初始化Cytoscape.js实例
const init_cyto = function () {
  cytoscape.use(coseBilkent);
  var cy = cytoscape({
    container: document.getElementById("cy"),
    elements: data,
    style: [
      {
        selector: "node",
        style: {
          "background-color": "#666",
          label: "data(id)",
        },
      },

      {
        selector: "edge",
        style: {
          width: 3,
          "line-color": "#ccc",
          "target-arrow-color": "#ccc",
          "target-arrow-shape": "triangle",
          "curve-style": "bezier",
        },
      },
    ],
  });
  document
    .getElementById("layoutButton")
    .addEventListener("click", function () {
      console.log("click layout button");
      var layout = cy.layout({
        name: "cose-bilkent",
        animate: "end",
        animationEasing: "ease-out",
        animationDuration: 1000 * 2,
        randomize: true,
      });

      layout.run();
    });
};
// 读取json，存入nodes和edges数据
const init_data = function () {
  var nodes, links, from, to;
  var node_degree = {};
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
    // 遍历原始nodes，去重并筛选需要的节点
    data = [];
    var idSet = new Set();
    nodes.forEach((node) => {
      var id = node.id.toString();
      // 第一个加入，后续重复的不管
      if (!idSet.has(id)) {
        if (id in node_degree) {
          var out_d = node_degree[id].out_degree;
          if (min <= out_d && out_d <= max) {
            // res.nodes.push(node);
            data.push({ data: { id: id } });
            idSet.add(id);
          }
        }
      }
    });
    links.forEach((link) => {
      from = link.source.toString();
      to = link.target.toString();
      if (idSet.has(from) && idSet.has(to)) {
        data.push({
          data: {
            id: from + "_" + to,
            source: from,
            target: to,
          },
        });
      }
    });
    // view data
    console.log(data);
  });
};

setTimeout(init_data, 100);
setTimeout(init_cyto, 200);
</script>
