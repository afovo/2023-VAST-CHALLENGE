<template>
  <div id="my_dataviz"></div>
</template>
<!--d3,用不了-->
<script setup>
import * as d3 from "d3";

const margin = {top: 30, right: 50, bottom: 10, left: 50},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

const svg = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/iris.csv").then(function(data) {
  const color = d3.scaleOrdinal()
      .domain(["setosa", "versicolor", "virginica"])
      .range(["#440154ff", "#21908dff", "#fde725ff"]);

  let dimensions = ["Petal_Length", "Petal_Width", "Sepal_Length", "Sepal_Width"];

  const y = {};
  for (let i in dimensions) {
    let name = dimensions[i];
    y[name] = d3.scaleLinear()
        .domain([0, 8])
        .range([height, 0]);
  }

  let x = d3.scalePoint()
      .range([0, width])
      .domain(dimensions);

  const highlight = function(event, d) {
    let selected_specie = d.Species;
    d3.selectAll(".line")
        .transition().duration(200)
        .style("stroke", "lightgrey")
        .style("opacity", "0.2");
    d3.selectAll("." + selected_specie)
        .transition().duration(200)
        .style("stroke", color(selected_specie))
        .style("opacity", "1");
  };

  const doNotHighlight = function(event, d) {
    d3.selectAll(".line")
        .transition().duration(200).delay(1000)
        .style("stroke", function(d) { return color(d.Species); })
        .style("opacity", "1");
  };

  function path(d) {
    return d3.line()(dimensions.map(function(p) { return [x(p), y[p](d[p])]; }));
  }

  svg.append("myPath")
      .data(data)
      .enter()
      .append("path")
      .attr("class", function(d) { return "line " + d.Species; })
      .attr("d", path)
      .style("fill", "red")
      .style("stroke", function(d) { return color(d.Species); })
      .style("opacity", 0.5)
      .on("mouseover", highlight)
      .on("mouseleave", doNotHighlight);

  svg.append("myAxis")
      .data(dimensions)
      .enter()
      .append("g")
      .attr("class", "axis")
      .attr("transform", function(d) { return `translate(${x(d)})`; })
      .each(function(d) { d3.select(this).call(d3.axisLeft().ticks(5).scale(y[d])); })
      .append("text")
      .style("text-anchor", "middle")
      .attr("y", -9)
      .text(function(d) { return d; })
      .style("fill", "black");
});
</script>

<style scoped>

</style>
