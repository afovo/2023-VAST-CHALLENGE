<template>
  <div id="bar-container" >
    <h4>{{title}}</h4>
  </div>
</template>
<script setup>
import * as d3 from 'd3'
import {defineProps, toRefs, watch} from "vue";
let height = 500, width = 500
let margin = ({top: 20, right: 0, bottom: 30, left: 40})

const props = defineProps({
  //子组件接收父组件传递过来的值
  rawData: Array,
  title: String
})
//使用父组件传递过来的值
const {rawData} =toRefs(props)
const {title} =toRefs(props)

const chart = function (){
  // d3.select("svg").remove();

  let data = [...rawData.value]
  for (let i = 0; i<data.length; i++) {
    data[i] = JSON.parse(JSON.stringify(data[i]))
  }
  console.log(data)
  let x = d3.scaleBand()
      .domain(data.map(d => d.name))
      .range([margin.left, width - margin.right])
      .padding(0.1)
  let y = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.value)]).nice()
      .range([height - margin.bottom, margin.top])
  let xAxis = g => g
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).tickSizeOuter(0))
  let yAxis = g => g
      .attr("transform", `translate(${margin.left},0)`)
      .call(d3.axisLeft(y))
      .call(g => g.select(".domain").remove())
  let svg = d3.select("#bar-container").append("svg")
      .attr("width", width)
      .attr("height", height)
      .call(zoom);

  svg.append("g")
      .attr("class", "bars")
      .attr("fill", "steelblue")
      .selectAll("rect")
      .data(data)
      .join("rect")
      .attr("x", d => x(d.name))
      .attr("y", d => y(d.value))
      .attr("height", d => y(0) - y(d.value))
      .attr("width", x.bandwidth());

  svg.exit().remove();

  svg.append("g")
      .attr("class", "x-axis")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y-axis")
      .call(yAxis);
  function zoom(svg) {
    const extent = [[margin.left, margin.top], [width - margin.right, height - margin.top]];

    svg.call(d3.zoom()
        .scaleExtent([1, 8])
        .translateExtent(extent)
        .extent(extent)
        .on("zoom", zoomed));

    function zoomed(event) {
      x.range([margin.left, width - margin.right].map(d => event.transform.applyX(d)));
      svg.selectAll(".bars rect").attr("x", d => x(d.name)).attr("width", x.bandwidth());
      svg.selectAll(".x-axis").call(xAxis);
    }
  }
}

watch(rawData, (newValue, oldValue) => {
  console.log(title.value,' chart update')
  chart()
});


</script>
<style scoped>
</style>

<style>
.chart div {
  font: 10px sans-serif;
  background-color: steelblue;
  text-align: right;
  padding: 10px;
  margin: 10px;
  color: white;
}
.container-chart {
  width: auto;
  margin: auto;
}
</style>
