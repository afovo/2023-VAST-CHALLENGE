<template>
  <div id="hierachy">
    <svg id="vizTreeV" />
  </div>
</template>
<style>
#vizTreeV circle {
  fill: #fff;
  stroke: #54a8ff;
  stroke-width: 3px;
}
#vizTreeV .node text {
  font: 12px sans-serif;
}
#vizTreeV .link {
  fill: none;
  stroke: #ccc;
  stroke-width: 2px;
}
</style>
<script setup>
import * as d3 from "d3";
import { defineProps, toRefs, watch, ref, defineExpose } from "vue";

const nodeType = ref({});
let defs;

async function init(fname, nodeID) {
  let nodesTypeIcons = ref({});
  await d3.json("data/Filter.json").then((data) => {
    nodesTypeIcons.value = data.nodesTypeIcons;
  });
  await d3.json("data/MC1.json").then((data) => {
    data.nodes.forEach((node) => {
      nodeType.value[node.id] = node.type;
    });
  });
  console.log(nodeType.value);
  let treeData = {};
  let svg;
  const anomalies = [
    "Mar de la Vida OJSC",
    "979893388",
    "Oceanfront Oasis Inc Carriers",
    "8327",
  ];
  await d3
    .json("data/hierachy/8327/hierachyData_ownership_" + fname + ".json")
    .then((data) => {
      treeData = data;
      let width = 1536;
      let height = 900;
      d3.select("#hierachy svg").remove();
      svg = d3
        .select("#hierachy")
        .append("svg")
        .attr("id", "vizTreeV")
        .attr("width", width)
        .attr("height", height);
      defs = svg.append("defs");
      // 添加 node icon
      Object.keys(nodesTypeIcons.value).forEach((nodeType) => {
        defs
          .append("symbol")
          .attr("id", nodeType)
          .append("svg")
          .attr("viewBox", "0 0 24 24")
          .append("path")
          .attr("d", nodesTypeIcons.value[nodeType]);
      });
      svg = svg.append("g");
      svg
        .transition()
        .duration(750)
        .attr("transform", "translate(" + 150 + "," + height / 2 + ")");
      ////////////// 初始化 全局zoom效果 //////////////
      // 创建缩放行为
      let zoom = d3.zoom();
      // 设置双击事件的处理函数
      zoom.on("zoom", (e) => {
        d3.select("#hierachy svg g").attr("transform", e.transform);
      });
      d3.select("#hierachy").call(zoom).on("dblclick.zoom", null);
      ////////////// 初始化 全局zoom效果 end //////////////

      var i = 0;
      var duration = 500;
      var root;

      // declares a tree layout and assigns the size
      var treemap = d3.tree().size([height, width]).nodeSize([40, 20]);
      // var treemap = d3.tree().nodeSize([width, height])

      // Assigns parent, children, height, depth
      root = d3.hierarchy(treeData, function (d) {
        return d.children;
      });

      root.x0 = height / 2;
      root.y0 = width / 2;

      // Collapse after the second level
      // root.children.forEach(collapse)

      update(root);

      // Collapse the node and all it's children
      function collapse(d) {
        if (d.children) {
          d._children = d.children;
          d._children.forEach(collapse); //_children:储存数据
          d.children = null; //children:用于渲染
        }
      }

      function update(source) {
        // Assigns the x and y position for the nodes
        var treeData = treemap(root);

        // Compute the new tree layout.
        var nodes = treeData.descendants();
        var links = treeData.descendants().slice(1);
        // console.log(nodes);
        // console.log(links);
        // Normalize for fixed-depth.
        nodes.forEach(function (d) {
          d.y = d.depth * 180;
        });

        // ****************** Nodes section ***************************

        // Update the nodes...
        var node = svg.selectAll("g.node").data(nodes, function (d) {
          return d.id || (d.id = ++i);
        });
        // console.log(node);
        // Enter any new modes at the parent's previous position.
        var nodeEnter = node
          .enter()
          .append("g")
          .attr("class", "node")
          .attr("transform", function () {
            return "translate(" + source.y0 + "," + source.x0 + ")";
          })
          .on("click", click);

        // Add Circle for the nodes
        nodeEnter
          .append("circle")
          .attr("r", 1e-6 * 2)
          .attr("class", "node")
          .append("circle")
          .attr("class", "node")
          .attr("r", 1e-6)
          .style("fill", function (d) {
            if (anomalies.includes(d.data.name)) {
              return d._children ? "#ff0000" : "#ff9999";
            } else if (d.data.name === nodeID.value.value) {
              return "blue";
            }
            return d._children ? "#c9e4ff" : "#fff";
          });

        // add svg icon for nodes
        nodeEnter
          .append("use")
          .attr("id", (d) => {
            return d.id;
          })
          .attr("width", 20)
          .attr("height", 20)
          .attr("xlink:href", (d) => {
            let type = nodeType.value[d.data.name];
            return type ? `#${type}` : `#null`;
          })
          .attr("transform", `translate(${-10},${-10})`);

        // Add labels for the nodes
        nodeEnter
          .append("text")
          .attr("text-anchor", function (d) {
            return d.children || d._children ? "center" : "start";
          })
          .text(function (d) {
            return d.data.name;
          })
          .attr("dy", (d) => {
            return d.children || d._children ? "25px" : "0.3rem";
          })
          .attr("dx", (d) => {
            return d.children || d._children
              ? `-${d.data.name.length / 4}em`
              : "15px";
          });

        // UPDATE
        var nodeUpdate = nodeEnter.merge(node);

        // Transition to the proper position for the node
        nodeUpdate
          .transition()
          .duration(duration)
          .attr("transform", function (d) {
            return "translate(" + d.y + "," + d.x + ")";
          });

        // Update the node attributes and style
        nodeUpdate
          .select("circle.node")
          .attr("r", 14)
          .style("fill", function (d) {
            //   console.log(d.data.name);
            if (anomalies.includes(d.data.name)) {
              return d._children ? "#ff9999" : "#ff0000";
            } else if (d.data.name === nodeID.value.value) {
              return "blue";
            }
            return d._children ? "#c9e4ff" : "#fff";
          })
          .style("stroke-width", function () {
            return "2px";
          })
          .attr("cursor", "pointer");

        // Remove any exiting nodes
        var nodeExit = node
          .exit()
          .transition()
          .duration(duration)
          .attr("transform", function () {
            return "translate(" + source.y + "," + source.x + ")";
          })
          .remove();

        // On exit #f7d708uce the node circles size to 0
        nodeExit.select("circle").attr("r", 1e-6);

        // On exit #f7d708uce the opacity of text labels
        nodeExit.select("text").style("fill-opacity", 1e-6);

        // ****************** links section ***************************

        // Update the links...
        var link = svg.selectAll("path.link").data(links, function (d) {
          return d.id;
        });

        // Enter any new links at the parent's previous position.
        var linkEnter = link
          .enter()
          .insert("path", "g")
          .attr("class", "link")
          .attr("d", function () {
            var o = { x: source.x0, y: source.y0 };
            return diagonal(o, o);
          });

        // UPDATE
        var linkUpdate = linkEnter.merge(link);

        // Transition back to the parent element position
        linkUpdate
          .transition()
          .duration(duration)
          .attr("d", function (d) {
            return diagonal(d, d.parent);
          });

        // Remove any exiting links
        link
          .exit()
          .transition()
          .duration(duration)
          .attr("d", function () {
            var o = { x: source.x, y: source.y };
            return diagonal(o, o);
          })
          .remove();

        // Store the old positions for transition.
        nodes.forEach(function (d) {
          d.x0 = d.x;
          d.y0 = d.y;
        });

        // Creates a curved (diagonal) path from parent to the child nodes
        function diagonal(s, d) {
          let path = `M ${s.y} ${s.x}
            C ${(s.y + d.y) / 2} ${s.x},
              ${(s.y + d.y) / 2} ${d.x},
              ${d.y} ${d.x}`;

          return path;
        }

        // Toggle children on click.
        function click(event, d) {
          console.log("click node");
          // console.log(d);
          d3.select(this)
            .select("circle")
            .transition()
            .delay(1)
            .style("fill", function () {
              return "#aaeeff";
            })
            .style("stroke-width", function () {
              return "3px";
            });
          if (d.children) {
            d._children = d.children;
            d.children = null;
          } else {
            d.children = d._children;
            d._children = null;
          }
          update(d);
        }
      }
    });
}

defineExpose({ init });
</script>
