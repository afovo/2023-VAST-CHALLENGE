<template>
  <div>min<el-input-number :min="0" :max="max" v-model="min" :step="1" /></div>
  <div>
    max<el-input-number :min="min" :max="400" v-model="max" :step="1" />
  </div>
  <div>
    clear <el-button type="primary" plain @click="clear">clear</el-button>
  </div>
  <div>
    submit <el-button type="primary" plain @click="cut">submit</el-button>
  </div>
  <div style="border: solid; height: 600px; width: 600px"></div>
</template>
<style scoped></style>
<script setup>
import * as d3 from "d3";
let data = $ref({});
let node_degree = $ref({});
let nodes = $ref([]);
let links = $ref([]);
let min = $ref(3);
let max = $ref(6);
let set = $ref();
let net = $ref();

const cut = function () {
  set = new Set();
  nodes = [];
  links = [];
  Object.keys(node_degree).forEach((d) => {
    if (node_degree[d] >= min && node_degree[d] <= max) {
      set.add(d);
    }
  });
  data.nodes.forEach((d) => {
    if (set.has(d.id)) {
      nodes.push(d);
    }
  });
  data.links.forEach((d) => {
    if (set.has(d.source) || set.has(d.target)) {
      links.push(d);
    }
  });
  console.log(`min:${min},max:${max}`);
  console.log(`nodes:${nodes.length}`);
  console.log(`links:${links.length}`);
  net = { nodes: nodes, links: links };
  console.log(net);
};

const clear = function () {
  min = 3;
  max = 6;
  cut();
};

d3.json("/MC1.json").then((d) => {
  data = d;
  data.links.forEach((d) => {
    let from = d.source;
    let to = d.target;
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
  cut();
});
</script>
