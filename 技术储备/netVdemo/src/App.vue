<template>
  <el-collapse v-model="activeNames">
    <!-- filter -->
    <el-collapse-item title="Filter" name="Filter">
      <Filter/>
    </el-collapse-item>
    <!-- ego net demo -->
    <el-collapse-item title="EgoNet" name="EgoNet">
      <EgoNet/>
    </el-collapse-item>
  </el-collapse>
</template>
<style scoped></style>
<script setup>
import EgoNet from "./components/ego.vue";
import Filter from "./components/filter.vue";
import * as d3 from "d3";

let activeNames = $ref(["Filter", "EgoNet"]);

let nodes = {}
let links = {}
let graph = {}

d3.json("../public/MC1.json").then(function (raw_data) {
  for (let i = 0; i < raw_data.nodes.length; i++) {
    nodes[raw_data.nodes[i].id] = raw_data.nodes[i]
  }
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
  }
  console.log('nodes: ')
  console.log(nodes)
  console.log('links: ')
  console.log(links)
  console.log('graph: ' )
  console.log(graph)
});

</script>
