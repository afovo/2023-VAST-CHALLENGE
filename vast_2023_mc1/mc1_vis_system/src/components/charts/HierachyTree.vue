<template>
  <div id="container">
    <div id="main">
      <svg id="vizTreeV" class="container-border" />
    </div>
  </div>
</template>
<style scoped>
#container {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  z-index: 0;
}
#main {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
}
</style>
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
<script>
import * as d3 from "d3";
export default {
  data() {
    return {};
  },
  mounted() {
    let treeData = {};
    d3.json("/8327/hierachyData_ownership_out.json").then((data) => {
      treeData = data;
      // console.log(data);
      var margin = { top: 420, right: 90, bottom: 90, left: 150 };

      let main = document.getElementById("main");
      main.parentElement.style.height = main.parentElement.style.width = "100%";
      main.style.height = main.style.width = "100%";
      let width = main.clientWidth;
      let height = main.clientHeight;

      var svg = d3
        .select("#vizTreeV")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      ////////////// 初始化 全局zoom效果 //////////////
      // 创建缩放行为
      let zoom = d3.zoom();
      // 设置双击事件的处理函数
      zoom.on("zoom", (e) => {
        d3.select("#main svg g").attr("transform", e.transform);
      });
      d3.select("#main").call(zoom).on("dblclick.zoom", null);
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
      // console.log(root);
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
            return d._children ? "#c9e4ff" : "#fff";
          });

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
            return d.children || d._children ? "20px" : "0.25rem";
          })
          .attr("dx", (d) => {
            return d.children || d._children
              ? `-${d.data.name.length / 4}em`
              : "13px";
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
          .attr("r", 10)
          .style("fill", function (d) {
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
          console.log(d);
          d3.select(this)
            .select("circle")
            .transition()
            .delay(1)
            .style("fill", function () {
              return "#6cfa00";
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
  },
};
</script>
