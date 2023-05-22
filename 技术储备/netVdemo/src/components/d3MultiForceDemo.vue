<template>
<body>
</body>
</template>

<script setup>
import * as d3 from 'd3'
var nodes = [{id:0}, {id:1}, {id:2}, {id:3}, {id:4}, {id:5}];
var links = [
  // one link
  { source: 0, target: 1 },

  // two links
  { source: 2, target: 1 },
  { source: 1, target: 2 },

  //three links
  { source: 3, target: 2 },
  { source: 2, target: 3 },
  { source: 2, target: 3 },

  // four links
  { source: 3, target: 4 },
  { source: 3, target: 4 },
  { source: 3, target: 4 },
  { source: 3, target: 4 },

  // five links
  { source: 4, target: 5 },
  { source: 4, target: 5 },
  { source: 4, target: 5 },
  { source: 4, target: 5 },
  { source: 4, target: 5 }
];

// DATA FORMATTING
links.forEach(function(link) {
  var same = links.filter((l)=>{return l.source === link.source && l.target === link.target});
  var sameAlt = links.filter((l)=>{return l.source === link.target && l.target === link.source});
  var sameAll = same.concat(sameAlt);

  sameAll.forEach(function(s, i) {
    s.sameIndex = (i + 1);
    s.sameTotal = sameAll.length;
    s.sameTotalHalf = (s.sameTotal / 2);
    s.sameUneven = ((s.sameTotal % 2) !== 0);
    s.sameMiddleLink = ((s.sameUneven === true) && (Math.ceil(s.sameTotalHalf) === s.sameIndex));
    s.sameLowerHalf = (s.sameIndex <= s.sameTotalHalf);
    s.sameArcDirection = s.sameLowerHalf ? 0 : 1;
    s.sameIndexCorrected = s.sameLowerHalf ? s.sameIndex : (s.sameIndex - Math.ceil(s.sameTotalHalf));
  });

  let sameStandard = sameAll[0];
  let sourceStandard = sameStandard.source;
  let targetStandard = sameStandard.target;
  sameAll.forEach(function(s){
    if(s.source === targetStandard && s.target === sourceStandard && s.sameTotal > 1){
      s.sameArcDirection = s.sameArcDirection === 0 ? 1 : 0
    }
  })
});
var maxSame = links.sort(function(a, b) {
  return a.sameTotal - b.sameTotal;
}).pop().sameTotal;
links.forEach(function(link) {
  link.maxSameHalf = Math.floor(maxSame / 2);
});


var width = 960,
    height = 500;
var simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(function(d) {return d.id; }).distance(50).strength(1))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force('charge', d3.forceManyBody().strength(-20))
    // 碰撞力 防止节点重叠
    .force('collide',d3.forceCollide().radius(20).iterations(2))
    .on('tick', tick);

let svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

let arrow = svg.append('defs')
    .append('marker')
    .attr('id', 'arrow')
    .attr("markerUnits","userSpaceOnUse")
    .attr("viewBox", "0 -5 10 10")//坐标系的区域
    .attr("refX",20)//箭头坐标
    .attr("refY", -1)
    .attr("markerWidth", 5)//标识的大小
    .attr("markerHeight", 5)
    .attr("orient", "auto")//绘制方向，可设定为：auto（自动确认方向）和 角度值
    .attr("stroke-width",0.2)//箭头宽度
    .append("path")
    .attr("d", "M0,-5L10,0L0,5")//箭头的路径
    .attr('fill','gray');

let link = svg.selectAll("path")
    .data(links)
    .enter()
    .append("path")
    .attr("class", function(d) { return "link " + d.type; })
    .attr("marker-end", "url(#arrow)")
    .style("stroke", 'green')
    .attr("fill", "none");

const node = svg.append("g")
    .selectAll("g")
    .data(nodes)
    .enter().append("g");

node.append("circle")
    .attr("r", 5)
    .attr("fill", "lightBlue")
node.call(
    d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended)
);


function tick() {
  link.attr("d", linkArc);
  node.call(updateNode);
  link.call(updateLink);
}

function linkArc(d) {
  var dx = (d.target.x - d.source.x),
      dy = (d.target.y - d.source.y),
      dr = Math.sqrt(dx * dx + dy * dy),
      unevenCorrection = (d.sameUneven ? 0 : 0.5),
      arc = ((dr * d.maxSameHalf) / (d.sameIndexCorrected - unevenCorrection));
  if (d.sameMiddleLink) {
    arc = 0;
  }
  return "M" + d.source.x + "," + d.source.y + "A" + arc + "," + arc + " 0 0," + d.sameArcDirection + " " + d.target.x + "," + d.target.y;
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
</script>

<style scoped>

</style>
