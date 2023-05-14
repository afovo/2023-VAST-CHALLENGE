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
let data = $ref();
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
        animationDuration: 1000 * 5,
        randomize: true,
      });

      layout.run();
    });
};
// 读取json，存入nodes和edges数据
const init_data = function () {
  data = [];
  d3.json("/mini.json").then(function (res) {
    var nodes = res.nodes;
    var links = res.links;
    nodes.forEach((e) => data.push({ data: { id: e.id.toString() } }));
    links.forEach((e) => {
      var from = e.source.toString();
      var to = e.target.toString();
      var id = from + "_" + to;
      data.push({ data: { id: id, source: from, target: to } });
    });
  });
};

setTimeout(init_data, 100);
setTimeout(init_cyto, 200);
</script>
