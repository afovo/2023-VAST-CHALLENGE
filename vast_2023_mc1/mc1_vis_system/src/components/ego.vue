<template>
  <div id="nodes-legend" style="position: absolute;left: 10%"></div>
  <div id="links-legend" style="position: absolute;left: 30%"></div>
  <div id="graph" ></div>
</template>

<script setup>
import * as d3 from 'd3'
import {toRefs, defineProps, watch} from 'vue'

let colorMap = new Map()//colorMap for links_data
colorMap.set("membership","#B0D6F7")
colorMap.set("partnership","#C1F7B0")
colorMap.set("ownership","#E0B0F7")
colorMap.set("family_relationship","#F7F3B0")
colorMap.set("undefined","#888888")

const person = function(){return d3.symbol().type((d) => {
  return {
    draw: (context, size) => {
      const r = Math.sqrt(2*size / 3);
      const x = -r / 2;
      const y = -r / 2;
      context.moveTo(x + r / 2, y);
      context.arc(x, y, r / 2, 0, Math.PI * 2);
      context.moveTo(x + r / 2, y + r);
      context.arc(x, y + r, r * 0.8, Math.PI, Math.PI * 2);
    }
  };
})};
const wye = function(){return d3.symbol().type(d3.symbolWye).size(80)};
const square = function(){return d3.symbol().type(d3.symbolSquare).size(80)};
const cross = function(){return d3.symbol().type(d3.symbolCross).size(80)};
const circle = function(){return d3.symbol().type(d3.symbolCircle).size(80)};
const semi = function(){return d3.symbol().type((d) => {
  return {
    draw: (context, size)=> {
      let r = Math.sqrt(2 * size / 3);
      let orgin = (4 * r) / (3 * Math.PI); //the orgin of the circle, not of the symbol
      context.arc(0, -orgin, r, Math.PI, 2 * Math.PI, true);
      context.closePath();
    }
  };
})};
const star = function(){return d3.symbol().type(d3.symbolStar).size(80)};
const triangle = function(){return d3.symbol().type(d3.symbolTriangle).size(80)};
const diamond = function(){return d3.symbol().type(d3.symbolDiamond).size(80)};

let shapeMap = new Map()//shapeMap for nodes_data
shapeMap.set("person", person());
shapeMap.set("organization", wye());
shapeMap.set("company", square());
shapeMap.set("political_organization", cross());
shapeMap.set("location", circle());
shapeMap.set("vessel", semi());
shapeMap.set("event", star());
shapeMap.set("movement", triangle());
shapeMap.set("undefined", diamond());


const props = defineProps({
  //子组件接收父组件传递过来的值
  nodesRawData: Array,
  linksRawData: Array
})
//使用父组件传递过来的值
const {nodesRawData} =toRefs(props)
const {linksRawData} =toRefs(props)


const draw = function () {
  d3.selectAll("svg").remove();

  ///////////图例///////////
  {
    const legend1 = d3.select("#nodes-legend")
        .append("svg")
        .attr("width", 400)
        .attr("height", 200);

    const legendItems1 = legend1.selectAll(".legend-item1")
        .data([...shapeMap])
        .enter()
        .append("g")
        .attr("class", "legend-item1")
        .attr("transform", (d, i) => `translate(9, ${i * 20+20})`);

    legendItems1.append("path")
        .attr("d", d=>d[1]())
        .style("fill", "#000")
        .style("stroke", "#000");

    legendItems1.append("text")
        .attr("x", 20)
        .attr("y", 10)
        .text(d => d[0]);


    const legend2 = d3.select("#links-legend")
        .append("svg")
        .attr("width", 100)
        .attr("height", 100);

    const legendItems = legend2.selectAll(".legend-item")
        .data([...colorMap])
        .enter()
        .append("g")
        .attr("class", "legend-item")
        .attr("transform", (d, i) => `translate(0, ${i * 20})`);

    legendItems.append("rect")
        .attr("width", 10)
        .attr("height", 10)
        .style("fill", d => d[1]);

    legendItems.append("text")
        .attr("x", 20)
        .attr("y", 10)
        .text(d => d[0]);
  }


  ///////////数据格式转换///////////
  let nodes_data = [...nodesRawData.value]
  for (let i = 0; i<nodes_data.length; i++) {
    nodes_data[i] = JSON.parse(JSON.stringify(nodes_data[i]))
  }

  let links_data = [...linksRawData.value]
  for (let i = 0; i<links_data.length; i++) {
    links_data[i] = JSON.parse(JSON.stringify(links_data[i]))
  }

  //////////多边弧线预处理START///////////
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
  //////////多边弧线预处理END///////////

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

  let arrow = svg.append("defs")//箭头
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

  ///////////边///////////
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

  ///////////节点///////////
  const nodes = svg.append("g")
      .attr("class", "nodes")
      .selectAll(".node")
      .data(nodes_data)
      .enter().append("g")
      .attr("class", function(d) {
        return d.type == null?"undefined node":d.type+" node";
      })
      .call(node => node.append("title").text(d => d.id))//鼠标hover显示title
      .call(//拖拽事件
      d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended)
      );

  for (let [key, value] of shapeMap) {//节点形状
    d3.selectAll('.'+key).append("path")
        .attr('d', value)
        .style("fill", d => {return d.color==null?'#666666':d.color});
  }



  function tick() {
    links.attr("d", linkArc);
    nodes.call(updateNode);
    links.call(updateLink);
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



// setTimeout(draw, 10)
watch(nodesRawData, (newValue, oldValue) => {
  console.log('ego update')
  draw()
});



</script>

<style scoped>

</style>
