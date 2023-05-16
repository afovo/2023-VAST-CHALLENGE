<template>
  <div>min<el-input-number :min="0" :max="max" v-model="min" :step="1" /></div>
  <div>
    max<el-input-number :min="min" :max="400" v-model="max" :step="1" />
  </div>
  <div>
    clear
    <el-button type="primary" plain @click="init_min_max">clear</el-button>
  </div>
  <div>
    submit
    <el-button type="primary" plain @click="cut_net_by_min_max"
      >submit</el-button
    >
  </div>
  <svg style="border: solid" width="600px" height="600px" id="main"></svg>
</template>
<style scoped></style>
<script setup>
import * as d3 from "d3";
let data = $ref({});
let node_degree = $ref({});
let temp_nodes = $ref([]);
let temp_links = $ref([]);
let min = $ref();
let max = $ref();
let set = $ref();
let graph = $ref();
let main, width, height;

const render_net = function () {
  console.log("render_net");
  main = d3.select("#main");
  width = main.attr("width");
  height = main.attr("height");
};

const cut_net_by_min_max = function () {
  set = new Set();
  temp_nodes = [];
  temp_links = [];
  graph = {};
  Object.keys(node_degree).forEach((d) => {
    if (node_degree[d] >= min && node_degree[d] <= max) {
      set.add(d);
    }
  });
  data.nodes.forEach((d) => {
    if (set.has(d.id.toString())) {
      temp_nodes.push({
        type: d.type,
        dataset: d.dataset,
        id: d.id.toString(),
      });
    }
  });
  data.links.forEach((d) => {
    if (set.has(d.source.toString()) && set.has(d.target.toString())) {
      temp_links.push({
        type: d.type,
        weight: d.weight,
        dataset: d.dataset,
        source: d.source.toString(),
        target: d.target.toString(),
        key: d.key,
      });
    }
  });
  console.log(`min:${min},max:${max}`);
  console.log(`nodes:${temp_nodes.length}`);
  console.log(`links:${temp_links.length}`);
  graph = { nodes: temp_nodes, links: temp_links };
  console.log(graph);
  render_net();
};

const init_min_max = function () {
  min = 3;
  max = 6;
  cut_net_by_min_max();
};

d3.json("/MC1.json").then((d) => {
  data = d;
  data.links.forEach((d) => {
    let from = d.source.toString();
    let to = d.target.toString();
    if (node_degree[from] == undefined) {
      node_degree[from] = 0;
    } else {
      node_degree[from]++;
    }
    if (node_degree[to] == undefined) {
      node_degree[to] = 0;
    } else {
      node_degree[to]++;
    }
  });
  init_min_max();
});
</script>
