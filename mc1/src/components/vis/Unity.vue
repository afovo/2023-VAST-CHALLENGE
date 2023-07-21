<template>
  <div id="unity"><svg></svg></div>
</template>
<style scoped></style>
<script setup>
import * as d3 from "d3";
import { ref, defineEmits } from "vue";
import router from "../../router";

let main, svg, nodesData, linksData, nodes, links, colorMap;
let simulation,
  tick,
  dragStart,
  drag,
  dragEnd,
  dragStartTime,
  hoverOn,
  hoverOut;
let nodeSizeScale, linkWidthScale;
let isRelationShip, isUnity, isNode, doubleClick;
let click, unfold, fold;
let lastClickNode = ref("");
const emit = defineEmits(["submit"]);
async function initFunction() {
  hoverOn = function (event, d) {
    d3.select(this).select("text").style("display", "inline");
  };
  hoverOut = function (event, d) {
    d3.select(this).select("text").style("display", "none");
  };
  colorMap = {
    "Companies (linked ownership)": "#DA70D6",
    "Organizations (linked ownership)": "#00FF7F",
    "People (linked family-relationship)": "#FF7F50",
    "Political Organization (linked ownership)": "#87CEEB",
  };
  nodeSizeScale = d3
    .scaleLog()
    .domain([1, d3.max(nodesData, (node) => node.size)])
    .range([15, 45]);
  linkWidthScale = d3
    .scaleLinear()
    .domain([0.1, d3.max(linksData, (link) => link.weight)])
    .range([1, 6]);
  tick = function () {
    nodes.attr("transform", function (d) {
      return `translate(${+d.x},${+d.y})`;
    });

    links.attr("d", function (d) {
      // return `M ${+d.source.x} ${+d.source.y} L ${+d.target.x} ${+d.target.y}`;
      // 计算起点和终点的中点坐标
      var midX = (d.source.x + d.target.x) / 2;
      var midY = (d.source.y + d.target.y) / 2;
      var sum = 0;
      var ram = d.source.id + d.target.id;
      for (var i = 0; i < ram.length; i++) {
        sum += ram.charCodeAt(i);
      }
      // 使用模板字符串生成弧形路径，控制点为起点和终点的中点
      var path = `M ${d.source.x} ${d.source.y}
      Q ${midX - sum / 400} ${midY - sum / 400}
      ${d.target.x} ${d.target.y}`;
      return path;
    });
  };
  dragStart = function (event, d) {
    event.sourceEvent.stopPropagation();
    if (!event.active) simulation.alphaTarget(0.01).restart();
    d.fx = d.x;
    d.fy = d.y;
    dragStartTime = new Date();
  };
  drag = function (event, d) {
    d.fx = event.x;
    d.fy = event.y;
  };
  dragEnd = function (event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
    new Date() - dragStartTime > 15 * 1000
      ? console.log("hold more than 15s " + d.id)
      : {};
  };
  unfold = async function (d) {
    console.log("unfold");
    if (isNode(d)) {
      return;
    } else if (isRelationShip(d)) {
      // 不是最小单元，是unity
      let prefix = d.id;
      // 重置 nodesData 数据
      nodesData = [];
      for (
        let unityIndex = 0;
        unityIndex < d.childrenUnity.length;
        unityIndex++
      ) {
        const unity = d.childrenUnity[unityIndex];
        nodesData.push({
          id: prefix + "***" + unityIndex,
          size: unity.length,
          childrenUnity: null,
          childrenNodes: new Set(unity.flat()),
          type: "",
        });
      }
    } else if (isUnity(d)) {
      // 最小单元，里面都是 node
      // 重置 nodesData 数据
      nodesData = [];
      [...d.childrenNodes].forEach((node) => {
        nodesData.push({
          id: node,
          size: 1,
          childrenUnity: null,
          childrenNodes: null,
          type: "",
        });
      });
    }
    // 加上这个点，方便返回
    d.type = "back";
    d.fx = d.fy = 100;
    nodesData.push(d);
    lastClickNode.value = d.id;
    // 重置 linksData 数据
    await getLinks();
    await initRender();
    await updateRender();
  };
  fold = async function (d) {
    console.log("fold");
    if (isRelationShip(d)) {
      await init();
    } else if (isUnity(d)) {
      await init();
      let data = null;
      nodesData.forEach((e) => {
        if (e.id == lastClickNode.value.split("***")[0]) {
          data = e;
          console.log(e);
        }
      });
      if (data != null) {
        await unfold(data);
      }
    }
  };
  click = async function (event, d) {
    d.type == "back" ? fold(d) : unfold(d);
  };
  doubleClick = async function (event, d) {
    console.log("db click");
    isNode(d) ? emit("submit", d.id) : {};
  };
}

async function getLinks() {
  // 遍历 links ，拿到四个点之间的连接
  await d3.json("data/MC1.json").then((data) => {
    linksData = [];
    let SOURCE_TARGET_WEIGHT = {};

    data.links.forEach((link) => {
      let sourceUnity = null;
      let targetUnity = null;
      let source = link.source;
      let target = link.target;
      let weight = link.weight;
      let nodeSet = new Set(nodesData.flatMap((e) => e.id));
      nodesData.forEach((node) => {
        // TODO: 分三种不同的情况加入 links
        if (isRelationShip(node) || isUnity(node)) {
          if (node.childrenNodes.has(source)) {
            sourceUnity = node.id;
          }
          if (node.childrenNodes.has(target)) {
            targetUnity = node.id;
          }
        } else if (isNode(node)) {
          if (nodeSet.has(source) && nodeSet.has(target)) {
            sourceUnity = source;
            targetUnity = target;
          }
        }
        if (
          sourceUnity != null &&
          targetUnity != null &&
          sourceUnity != targetUnity
        ) {
          if (SOURCE_TARGET_WEIGHT[`${sourceUnity}^^^${targetUnity}`]) {
            SOURCE_TARGET_WEIGHT[`${sourceUnity}^^^${targetUnity}`] += weight;
          } else {
            SOURCE_TARGET_WEIGHT[`${sourceUnity}^^^${targetUnity}`] = weight;
          }
        }
      });
    });

    Object.keys(SOURCE_TARGET_WEIGHT).forEach((key) => {
      linksData.push({
        source: key.split("^^^")[0],
        target: key.split("^^^")[1],
        weight: SOURCE_TARGET_WEIGHT[key],
      });
    });
  });
}

async function initData() {
  // 先从 unities 拿到 unity node 数据
  await d3.json("data/unities.json").then((data) => {
    nodesData = [];
    data.forEach((node) => {
      nodesData.push({
        id: node.name,
        size: node.size,
        childrenUnity: node.unity,
        childrenNodes: new Set(node.unity.flat()),
        type: "",
      });
    });
  });
  await getLinks();
}

async function initRender() {
  d3.select("#unity svg").remove();
  svg = d3
    .select("#unity")
    .append("svg")
    .attr("width", 1536)
    .attr("height", 900)
    .append("g");
  // 添加全局zoom效果
  d3.select("#unity svg")
    .call(
      d3.zoom().on("zoom", (e) => {
        d3.select("#unity svg g").attr("transform", e.transform);
      })
    )
    .on("dblclick.zoom", null);
  // init links
  links = svg
    .append("g")
    .attr("id", "links")
    .selectAll("path")
    .data(linksData)
    .enter()
    .append("path")
    .attr("fill", "none")
    .attr("stroke", "grey")
    .attr("stroke-width", (d) => linkWidthScale(d.weight))
    .style("opacity", "0.5");
  // init nodes
  nodes = svg
    .append("g")
    .attr("id", "nodes")
    .selectAll()
    .data(nodesData)
    .enter()
    .append("g")
    .on("dblclick", doubleClick)
    .on("click", click)
    .on("mouseover", hoverOn)
    .on("mouseout", hoverOut);

  nodes
    .append("circle")
    .attr("id", (d) => d.id)
    .attr("r", (d) => nodeSizeScale(d.size))
    .attr("fx", (d) => {
      if (d.type == "back") return 5;
    })
    .attr("fill", (d) => {
      if (isRelationShip(d)) {
        return colorMap[d.id];
      } else if (isUnity(d)) {
        return colorMap[d.id.split("***")[0]];
      } else {
        return colorMap[lastClickNode.value.split("***")[0]];
      }
    })
    .attr("stroke", (d) => {
      return d.type === "back" ? "red" : "black";
    })
    .attr("stroke-width", (d) => {
      return d.type === "back" ? 5 : 1;
    })
    .call(d3.drag().on("start", dragStart).on("drag", drag).on("end", dragEnd));

  nodes
    .append("text")
    .text((d) => {
      return d.id;
    })
    .attr("dy", (d) => nodeSizeScale(d.size) + 20)
    .attr("fill", "black")
    .attr("text-anchor", "start")
    .style("font-size", 20)
    .style("display", "none");
}

async function updateRender() {
  // init simulation
  simulation = d3
    .forceSimulation(nodesData)
    .force("charge", d3.forceManyBody().strength(-40))
    .force("collide", d3.forceCollide().radius(30).iterations(50))
    .force(
      "link",
      d3
        .forceLink(linksData)
        .id((d) => d.id)
        .distance(300)
        .strength(1.5)
    )
    .force("center", d3.forceCenter(1536 / 2, 900 / 2))
    .on("tick", tick);
}

async function init() {
  isRelationShip = (d) => {
    return d.childrenUnity != null && d.childrenNodes != null;
  };
  isUnity = (d) => {
    return d.childrenUnity == null && d.childrenNodes != null;
  };
  isNode = (d) => {
    return d.childrenUnity == null && d.childrenNodes == null;
  };
  await initData();
  await initFunction();
  await initRender();
  await updateRender();
}

init();
</script>
