<template>
  <div id="graph" ></div>
  <h4>nodes:</h4>
  <div>{{nodesRawData}}</div>
  <h4>links:</h4>
  <div>{{linksRawData}}</div>
</template>

<script setup>
import * as d3 from 'd3'
import {toRefs, defineProps, watch} from 'vue'

let colorMap = new Map()//colorMap for links_data
colorMap.set("membership","#B0D6F7")
colorMap.set("partnership","#C1F7B0")
colorMap.set("ownership","#E0B0F7")
colorMap.set("family_relationship","#F7F3B0")
colorMap.set("","#000000")


const props = defineProps({
  //子组件接收父组件传递过来的值
  nodesRawData: Array,
  linksRawData: Array
})
//使用父组件传递过来的值
const {nodesRawData} =toRefs(props)
const {linksRawData} =toRefs(props)


//
// d3.json("/mini.json").then(function (raw_data) {
//   let target = raw_data["8327"];
//   let nodes_data = [{id:"8327"}];
//   target["first"].forEach(function(d){
//     nodes_data.push({id:d,type:"membership"})
//   });
//   target["second"].forEach(function(d){
//     nodes_data.push({id:d,type:""})
//   });
//   let links_data = target["first_link"].concat(target["second_link"])
//   console.log(nodes_data)
//   // DATA FORMATTING
const draw = function () {
  d3.select("svg").remove();

  //数据格式转换
  let nodes_data = [...nodesRawData.value]
  for (let i = 0; i<nodes_data.length; i++) {
    nodes_data[i] = JSON.parse(JSON.stringify(nodes_data[i]))
  }

  let links_data = [...linksRawData.value]
  for (let i = 0; i<links_data.length; i++) {
    links_data[i] = JSON.parse(JSON.stringify(links_data[i]))
  }


  //test data
  //   nodes_data = [{id:0}, {id:1}, {id:2}, {id:3}, {id:4}, {id:5}];
//   links_data = [
//   // one link
//   { source: 0, target: 1 },
//
//   // two links
//   { source: 2, target: 1 },
//   { source: 1, target: 2 },
//
//   //three links
//   { source: 3, target: 2 },
//   { source: 2, target: 3 },
//   { source: 2, target: 3 },
//
//   // four links
//   { source: 3, target: 4 },
//   { source: 3, target: 4 },
//   { source: 3, target: 4 },
//   { source: 3, target: 4 },
//
//   // five links
//   { source: 4, target: 5 },
//   { source: 4, target: 5 },
//   { source: 4, target: 5 },
//   { source: 4, target: 5 },
//   { source: 4, target: 5 }
// ];

  links_data.forEach(function (link) {
    let same = links_data.filter((l) => {
      return l.source === link.source && l.target === link.target
    });
    let sameAlt = links_data.filter((l) => {
      return l.source === link.target && l.target === link.source
    });
    let sameAll = same.concat(sameAlt);
    sameAll.forEach(function (s, i) {
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
    sameAll.forEach(function (s) {
      if (s.source === targetStandard && s.target === sourceStandard && s.sameTotal > 1) {
        s.sameArcDirection = s.sameArcDirection === 0 ? 1 : 0
      }
    })
  });
  let maxSame = links_data.sort(function (a, b) {
    return a.sameTotal - b.sameTotal;
  })[links_data.length-1].sameTotal;
  links_data.forEach(function (link) {
    link.maxSameHalf = Math.floor(maxSame / 2);
  });

  // console.log(nodes_data)
  // console.log(links_data)
  let width = window.innerWidth,
      height = 500;
  let simulation = d3.forceSimulation()
      .nodes(nodes_data)
      .force("link", d3.forceLink(links_data).id(function (d) {
        return d.id;
      }).distance(50).strength(1))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force('charge', d3.forceManyBody().strength(-10))
      // 碰撞力 防止节点重叠
      .force('collide', d3.forceCollide().radius(20).iterations(2))
      .on('tick', tick);


  let svg = d3.select("#graph").append("svg")
      .attr("width", width)
      .attr("height", height);

  let arrow = svg.append("defs")
      .append("marker")
      .attr('id', 'arrow')
      .attr("markerUnits", "userSpaceOnUse")
      .attr("viewBox", "0 -5 10 10")//坐标系的区域
      .attr("refX", 20)//箭头坐标
      .attr("refY", -1)
      .attr("markerWidth", 5)//标识的大小
      .attr("markerHeight", 5)
      .attr("orient", "auto")//绘制方向，可设定为：auto（自动确认方向）和 角度值
      .attr("stroke-width", 0.2)//箭头宽度
      .append("path")
      .attr("d", "M0,-5L10,0L0,5")//箭头的路径
      .attr('fill', 'gray');

  console.log(links_data)
  let links = svg.append("g")
      .selectAll("path")
      .data(links_data)
      .enter()
      .append("path")
      .attr("class", function (d) {
        return "link " + d.type;
      })
      .attr("marker-end", "url(#arrow)")
      .attr("stroke", (d) => {
        return colorMap.get(d.type)
      })
      .attr("fill", "none");

  const nodes = svg.append("g")
      .selectAll("g")
      .data(nodes_data)
      .enter().append("g")
      .call(node => node.append("title").text(d => d.id));

  nodes.append("circle")
      .attr("r", 5)
      .attr("fill", 'black')/*(d) => {
        return colorMap.get(d.type)
      }*/
  nodes.call(
      d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended)
  );

  function tick() {
    links.attr("d", linkArc);
    nodes.call(updateNode);
    links.call(updateLink);
  }

  function linkArc(d) {
    let dx = (d.target.x - d.source.x),
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
    link.attr("x1", function (d) {
      return fixna(d.source.x);
    })
        .attr("y1", function (d) {
          return fixna(d.source.y);
        })
        .attr("x2", function (d) {
          return fixna(d.target.x);
        })
        .attr("y2", function (d) {
          return fixna(d.target.y);
        });
  }

  function updateNode(node) {
    node.attr("transform", function (d) {
      return "translate(" + fixna(d.x) + "," + fixna(d.y) + ")";
    });
  }

//////////////dragging////////////////////////
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

setTimeout(draw, 10)
watch(nodesRawData, (newValue, oldValue) => {
  console.log('hey')
  draw()
});



</script>

<style scoped>

</style>
