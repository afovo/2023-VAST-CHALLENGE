<template>
  <div class="slider-demo-block">
    <span class="demonstration">TimeLine</span>
    <el-slider v-model="index" :min="min" :max="max" :step="1" :format-tooltip="function(value){return times[value];}" show-stops />
<!--    <el-button-group>-->
<!--      <el-button :icon="Minus" @click="decrease" />-->
<!--      <el-button :icon="Plus" @click="increase" />-->
<!--    </el-button-group>-->
  </div>
  <div id="forceGraph" ></div>
</template>

<script setup>
import * as d3 from "d3";
import {ref, watch} from 'vue'
import { Minus, Plus } from '@element-plus/icons-vue'
const width = window.innerWidth;
const height = window.innerHeight;
let times = [];
let min=0;
let max=100;
let index = ref(0);
const increase = () => {
  index.value ++;
  if (index.value >= times.length) {
    index.value = times.length-1
  }
}
const decrease = () => {
  index.value--;
  if (index.value < 0) {
    index.value = 0
  }
}
const chart = function(){
  console.log("chart")
  d3.select("svg").remove();
  const svg = d3.select("body").append("svg")
      .attr("viewBox", [-width / 2, -height / 2, width, height]);
  console.log(svg)
  let link = svg.append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .selectAll("line");
  console.log(link)
  let node = svg.append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .selectAll("circle");
  console.log(node)
  const simulation = d3.forceSimulation()
      .force("charge", d3.forceManyBody())
      .force("link", d3.forceLink().id(d => d.id))
      .force("x", d3.forceX())
      .force("y", d3.forceY())
      .on("tick", ticked);

  function ticked() {
    node.attr("cx", d => d.x)
        .attr("cy", d => d.y);

    link.attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
  }
  return Object.assign(svg.node(), {
    update(nodes,links) {
      console.log("hey")

      // Make a shallow copy to protect against mutation, while
      // recycling old nodes to preserve position and velocity.
      const old = new Map(node.data().map(d => [d.id, d]));
      nodes = nodes.map(d => Object.assign(old.get(d.id) || {}, d));
      links = links.map(d => Object.assign({}, d));

      node = node
          .data(nodes, d => d.id)
          .join(enter => enter.append("circle")
              .attr("r", 5)
              .call(drag(simulation))
              .call(node => node.append("title").text(d => d.id)));
      console.log(node.data())
      link = link
          .data(links, d => [d.source, d.target])
          .join("line");

      simulation.nodes(nodes);
      simulation.force("link").links(links);
      simulation.alpha(1).restart().tick();
      ticked(); // render now!
    }
  });
}

const contains = ({start, end}, time) => start <= time && time < end;
const init = function(){
  d3.json("/sfhh@4.json").then((res)=>{
    // const data = res
    const data = JSON.parse(JSON.stringify(res), (key, value) => key === "start" || key === "end" ? new Date(value) : value)
    console.log(data)
    function update(){
      const nodes = data.nodes.filter(d => contains(d, times[index.value]));
      const links = data.links.filter(d => contains(d, times[index.value]));
      chart().update(nodes,links);
    }
    watch(()=>index.value,
        (newValue, OldValue) => {
          update();
    })
    times = d3.scaleTime()
        .domain([d3.min(data.nodes, d => d.start), d3.max(data.nodes, d => d.end)])
        .ticks(1000)
        .filter(time => data.nodes.some(d => contains(d, time)));
    max = times.length-1
    console.log(times)
  })
}
const drag = simulation => {
  function dragstarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
  }

  function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }

  return d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
}
setTimeout(init,0)
</script>

<style scoped>
.slider-demo-block {
  position: absolute;
  left: 10%;
  top:5%;
  width: 80%;
}
.slider-demo-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
}
.slider-demo-block .demonstration {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  line-height: 44px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 0;
}
.slider-demo-block .demonstration + .el-slider {
  flex: 0 0 70%;
}
</style>
