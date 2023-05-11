<template>
  <div class="chart-wrapper">
    <div id="line-chart" class="chart"></div>
  </div>
</template>
<style scoped>
.chart-wrapper {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
<script setup>
import * as d3 from "d3";

const lineData = [
  {
    values: [
      { date: "2020/01/01", total: 230 },
      { date: "2020/02/01", total: 290 },
      { date: "2020/03/01", total: 230 },
      { date: "2020/04/01", total: 270 },
      { date: "2020/05/01", total: 244 },
      { date: "2020/06/01", total: 270 },
      { date: "2020/07/01", total: 320 },
      { date: "2020/08/01", total: 320 },
      { date: "2020/09/01", total: 250 },
      { date: "2020/10/01", total: 272 },
    ],
  },
];

const init = function () {
  // Selecting the element
  const element = document.getElementById("line-chart");

  // Setting dimensions
  const margin = { top: 40, right: 30, bottom: 7, left: 50 },
    width = 900 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

  // Parsing timestamps
  const parseTime = d3.timeParse("%Y/%m/%d");

  const parsedData = lineData.map((item) => ({
    values: item.values.map((val) => ({
      total: val.total,
      date: parseTime(val.date),
    })),
  }));

  // Appending svg to a selected element
  const svg = d3
    .select(element)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", 300 + margin.top + margin.bottom)
    .attr("viewBox", `0 40 ${width + 80} ${height}`)
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

  // Setting X,Y scale ranges
  const xScale = d3
    .scaleTime()
    .domain([
      d3.min(parsedData, (d) => d3.min(d.values, (v) => v.date)),
      d3.max(parsedData, (d) => d3.max(d.values, (v) => v.date)),
    ])
    .range([0, width]);

  const yScale = d3
    .scaleLinear()
    .domain([
      d3.min(parsedData, (d) => d3.min(d.values, (v) => v.total)),
      d3.max(parsedData, (d) => d3.max(d.values, (v) => v.total)),
    ])
    .range([height, 0]);

  const chartSvg = svg.selectAll(".line").data(parsedData).enter();

  // Drawing line with inner gradient and area
  // Adding functionality to make line and area curved
  const line = d3
    .line()
    .x(function (d) {
      return xScale(d.date);
    })
    .y(function (d) {
      return yScale(d.total);
    })
    .curve(d3.curveCatmullRom.alpha(0.5));

  // Defining the area, which appear after animation ends
  const area = d3
    .area()
    .x(function (d) {
      return xScale(d.date);
    })
    .y0(height)
    .y1(function (d) {
      return yScale(d.total);
    })
    .curve(d3.curveCatmullRom.alpha(0.5));

  // Defining the line path and adding some styles
  const path = chartSvg
    .append("path")
    .attr("d", function (d) {
      return line(d.values);
    })
    .attr("stroke-width", "2")
    .style("fill", "none")
    .attr("stroke", "#ff6f3c");

  // Drawing animated area
  chartSvg
    .append("path")
    .attr("d", function (d) {
      return area(d.values);
    })
    .style("fill", "rgba(255,111,60,0.15)");

  // Adding the x Axis
  svg
    .append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xScale));

  // Adding the y Axis
  svg.append("g").call(d3.axisLeft(yScale));
};

setTimeout(init, 1);
</script>
