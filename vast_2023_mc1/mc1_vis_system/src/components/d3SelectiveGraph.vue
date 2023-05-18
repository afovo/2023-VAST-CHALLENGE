<template>
  {{node_id}}
  <button @click="selectId">Mar de la Vida OJSC</button>
  <div id="forceGraph" ></div>
</template>

<script setup>
import * as d3 from "d3";
import {ref, watch} from 'vue'
const width = window.innerWidth;
const height = window.innerHeight;
let node_id = ref(0);
let layer = ref(1);

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
    update(nodes,links) {//用chart().update调用
      // 浅拷贝，复用相对位置和力
      const old = new Map(node.data().map(d => [d.id, d]));
      nodes = nodes.map(d => Object.assign(old.get(d.id) || {}, d));
      links = links.map(d => Object.assign({}, d));
      node = node
          .data(nodes, d => d.id)
          .join(enter => enter.append("circle")
              .attr("r", 5)
              .call(drag(simulation))
              .call(node => node.append("title").text(d => d.id)));
      link = link
          .data(links, d => [d.source, d.target])
          .join("line");

      simulation.nodes(nodes);
      simulation.force("link").links(links);
      simulation.alpha(1).restart().tick();
      ticked(); // 立即渲染
    }
  });
}
const selectId = function (){
  node_id.value = "Mar de la Vida OJSC";
}
const init = function(){
  d3.json("./MC1.json").then((res)=>{
    const data = res
    console.log(data)
    //监听node_id
    watch(()=>node_id.value,
        (newValue, OldValue) => {
          console.log(data.links)
          const links = data.links.filter(d => d.source === node_id.value || d.target === node_id.value);
          // console.log(links)
          let map = new Map()
          links.forEach(function getNodes(d){
            map.set(d.source, 1);
            map.set(d.target, 1);
          })
          const nodes = data.nodes.filter(d => map.get(d.id)!=null);
          chart().update(nodes,links);
    })
  })
}
//拖拽
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
</style>
