<template>
  <div id="graph" style="width: 100%;height: 100%">
  </div>
</template>

<script setup>
import * as d3 from "d3";
const render = function() {
  const width = window.innerWidth, height = window.innerHeight;

  const color = d3.scaleOrdinal(d3.schemeCategory10);

  const shapeMap = new Map();
  shapeMap.set("Article","circle")
  // shapeMap.set()

  const types = ["CITED_BY"]

  const strokeWidth = 1.5


  // d3.json("/api/article/graph").then(function(data) {
/*ToDo:
   1. load /MC1 and draw
   2. map each node type(person, organization, company, political_organization, location, vessel, event, movement, undefined)
      to different d3 shapes
   3. map each edge type(membership, partnership, ownership, family_relationship) to different colors(已写
*/
  // let graph = data.data;
  let graph = {
    "links": [
      { "source": "18470926", "target": "10097404", "type": "CITED_BY" }
    ],
    "nodes": [
      {
        "label": "Article",
        "id": "18470926"
      },
      {
        "label": "Article",
        "id": "10097404"
      }
    ]
  };
  const simulation = d3.forceSimulation(graph.nodes)
      .force("charge", d3.forceManyBody().strength(-3000))
      .force("x", d3.forceX(width / 2).strength(1))
      .force("y", d3.forceY(height / 2).strength(1))
      .force("link", d3.forceLink(graph.links).id(function(d) {return d.id; }).distance(50).strength(1))
      .on("tick", ticked);

  const svg = d3.select("#graph").append("svg")
      .attr("width", width).attr("height",height)
      .attr("pointer-events", "all");

  // Per-type markers, as they don't inherit styles.
  svg.append("defs").selectAll("marker")
      .data(types)//箭头
      .join("marker")
      .attr("id", d => `arrow-${d}`)
      .attr("viewBox", "0 0 10 10")
      .attr("refX", 10)
      .attr("refY", 5)
      .attr("markerUnits", "strokeWidth")
      .attr("markerWidth", 10)
      .attr("markerHeight", 10)
      .attr("orient", "auto")
      .append("path")
      .attr("fill", color)
      .attr("d", 'M 0 0 L 10 5 L 0 10 z');

  const link = svg.append("g")
      .selectAll("g")
      .data(graph.links)
      .enter()
      .append("line")
      .attr("stroke", d => color(d.type))//assign different colors to different edges
      .attr("stroke-width", strokeWidth)
      .attr("marker-end", d => `url(${new URL(`#arrow-${d.type}`, location)})`);

  const node = svg.append("g")
      .selectAll("g")
      .data(graph.nodes)
      .enter().append("g");

  //node shape
  node.append("circle")
      .attr("r", 5)
      .attr("fill", "lightBlue")
  /*
You can change the shape of nodes in a force directed graph drawn by d3 v7 by using the d3.symbol() function1.

Here’s an example of how you can add two different shapes to a d3 force directed graph based on a shape field2:

var node = svg.selectAll(".node")
    .data(data.nodes)
    .enter().append("path")
    .attr("class", "node")
    .attr("d", d3.symbol()
        .type(function(d) { return d3.symbolTypes[d.s]; }))
    .style("fill", function(d) { return color(d.group); })
    .call(force.drag);
 */

  node.call(
      d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended)
  );
  node.append("text")
      .text(function(d) {
        return d.id;
      })
      .attr('x', 6)
      .attr('y', 3).style('fill', 'black');

  node.append("title")
      .text(function(d) { return d.label; });




  //force simulation rendering
  function ticked() {
    node.call(updateNode);
    link.call(updateLink);
  }

  function fixna(x) {
    if (isFinite(x)) return x;
    return 0;
  }

  function updateLink(link) {
    link.attr("x1", function(d) { return fixna(d.source.x); })
        .attr("y1", function(d) { return fixna(d.source.y); })
        .attr("x2", function(d) { return fixna(d.target.x); })
        .attr("y2", function(d) { return fixna(d.target.y); });
  }

  function updateNode(node) {
    node.attr("transform", function(d) {
      return "translate(" + fixna(d.x) + "," + fixna(d.y) + ")";
    });
  }

  //dragging
  function dragstarted(event, d) {
    event.sourceEvent.stopPropagation();
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
}
setTimeout(render, 1);
</script>

<style scoped>
</style>
