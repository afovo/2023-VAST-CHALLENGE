<template>
  <div>
    <svg ref="chartRef" />
  </div>
</template>

<script>
import * as d3 from "d3";

export default {
  data() {
    return {
      data:null,
      forceSimulation: null,
      links: null,
      linksText: null,
      gs: null,
      svg: null,
    };
  },
  // props: ["data"],
  watch: {
    data: {
      handler(newone, oldone) {
        if (newone !== null) this.draw();
      },
      immediate: true,
      deep: true,
    },
  },
  mounted() {
    this.data ={
      "nodes": [
        {
          "type": "company",
          "dataset": "MC1",
          "country": "Nalakond",
          "id": "Spanish Shrimp  Carriers"
        },
        { "type": "organization", "dataset": "MC1", "id": 12744 }
      ],
      "links": [
        {
          "type": "ownership",
          "weight": 0.90013963,
          "dataset": "MC1",
          "source": "Spanish Shrimp  Carriers",
          "target": 12744,
          "key": 0
        },
        {
          "type": "family_relationship",
          "weight": 0.90013963,
          "dataset": "MC1",
          "source": 12744,
          "target": "Spanish Shrimp  Carriers",
          "key": 0
        }
      ]
    }

    if (this.data) {
      this.draw();
    }
    window.onresize = () => {
      return (() => {
        if (this.data) this.draw();
        window.screenWidth = document.body.clientWidth;
      })();
    };
  },
  methods: {
    //根据不同方向分为 linkA，linkB 两个数组，分别分配两种 linknum，从而控制上下椭圆弧
    setLinkNumbers(group) {
      const len = group.length;
      const linksA = [];
      const linksB = [];
      for (let i = 0; i < len; i++) {
        const link = group[i];
        if (link.source.toString() < link.target.toString()) {
          linksA.push(link);
        } else {
          linksB.push(link);
        }
      }
      let startLinkANumber = 1;
      linksA.forEach((linkA) => {
        linkA.linknum = startLinkANumber++;
      });
      let startLinkBNumber = -1;
      linksB.forEach((linkB) => {
        linkB.linknum = startLinkBNumber--;
      });
    },
    draw() {
      this.nodes = JSON.parse(JSON.stringify(this.data.nodes));
      this.edges = JSON.parse(JSON.stringify(this.data.links));
      console.log(this.nodes)
      console.log(this.edges)
      if (this.svg) this.$refs.chartRef.childNodes.forEach((i) => i.remove());

      // const containerWidth = this.$refs.chartRef.parentElement.offsetWidth;
      // const containerHeight = this.$refs.chartRef.parentElement.offsetHeight;
      const containerWidth = 1000;
      const containerHeight = 500;
      const margin = { top: 0, right: 0, bottom: 0, left: 0 };
      const width = containerWidth - margin.left - margin.right;
      const height = containerHeight - margin.top - margin.bottom;
      this.svg = d3
          .select(this.$refs.chartRef)
          .attr("width", width)
          .attr("height", height);
      const marge = { top: 10, bottom: 10, left: 10, right: 10 };
      const g = this.svg
          .append("g")
          .attr("transform", "translate(" + marge.top + "," + marge.left + ")");

      this.forceSimulation = d3
          .forceSimulation()
          .force(
              "link",
              d3.forceLink().id((d) => {
                return d.id;
              })
          )
          .force("center", d3.forceCenter(width / 2, height / 2))
          .force('charge', d3.forceManyBody().strength(-20))
          // 碰撞力 防止节点重叠
          .force('collide',d3.forceCollide().radius(20).iterations(2));

      const linkGroup = {};
      // 两点之间的线根据两点的 id 属性设置为同一个 key，加入到 linkGroup 中，给两点之间的所有边分成一个组
      this.edges.forEach((link) => {
        const key =
            link.source.toString() < link.target.toString()
                ? link.source + ":" + link.target
                : link.target + ":" + link.source;
        if (!linkGroup.hasOwnProperty(key)) {
          linkGroup[key] = [];
        }
        linkGroup[key].push(link);
        link.size = linkGroup[key].length;
        const group = linkGroup[key];
        const keyPair = key.split(":");
        let type = "noself";
        if (keyPair[0] === keyPair[1]) {
          type = "self";
        }
        this.setLinkNumbers(group, type);
      });

      this.forceSimulation.nodes(this.nodes).on("tick", this.ticked);
      this.forceSimulation
          .force("link")
          .links(this.edges)
          .distance((d) => {
            return d.weight*250;
          });

      var line = d3.line()
          .curve(d3.curveCatmullRom.alpha(1));

      this.links = g
          .append("g")
          .selectAll("line")
          .data(this.edges)
          .enter()
          .append("line")
          .style("stroke", "#9aaabf")
          .style("stroke-width", 1)
          .style("fill-opacity", 0)
          .attr("id", function(d, i) {
            return "line" + i;
          })
          .style("cursor", "pointer")
          .attr('d', line);

      this.linksText = g
          .append("g")
          .selectAll("text")
          .data(this.edges)
          .enter()
          .append("text")
          .style("pointer-events", "none")
          .attr("class", "line-text")
          .style("cursor", "pointer")
          .attr("pointer-events", "none")
          .attr("xlink:href", function(d, i) {
            return "#line" + i;
          })
          .text((d) => {
            return d.type;
          });

      this.gs = g
          .selectAll(".circleText")
          .data(this.nodes)
          .enter()
          .append("g")
          .style("cursor", "pointer")
          .attr("transform", (d, i) => {
            return "translate(" + d.x + "," + d.y + ")";
          })
          .call(
              d3
                  .drag()
                  .on("start", this.dragStarted)
                  .on("drag", this.dragged)
                  .on("end", this.dragEnded)
          )
          .on("click", (e, g) => {
            this.$emit("nodeClicked", g);
          })
          .on("dblclick", (e, g) => {
            this.$emit("nodeDBLClicked", g);
          });

      this.gs
          .append("circle")
          .attr("class", "circle")
          .attr("r", 20)
          .attr("fill", (d, i) => {
            return this.colorScale(d.type);
          })
          .on("click", (e, g) => {
            this.$emit("nodeClicked", g);
          })
          .on("dblclick", (e, g) => {
            this.$emit("nodeDBLClicked", g);
          });

      this.gs
          .append("text")
          .attr("dy", ".35em")
          .attr("text-anchor", "middle")
          .style("fill", "#FFFFFF")
          .attr("font-size", 12)
          .attr("color", "white")
          .text((d) => {
            return d.id;
          });
    },
    colorScale(type) {
      switch (type) {
        case "company":
          return "#a3f304";
        case "organization":
          return "#ffa1a1";
        case "director":
          return "#a059f3";
        case "Movie":
          return "#14ffc9";
        case "author":
          return "#84ffc9";
        case "Community-Host":
          return "#a059f3";
        default:
          return "#ffa306";
      }
    },
    dragStarted(event) {
      event.sourceEvent.stopPropagation();
      if (!event.active) this.forceSimulation.alphaTarget(0.8).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    },
    dragged(event) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    },
    dragEnded(event) {
      if (!event.active) this.forceSimulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    },

    ticked() {
      // this.links.forEach(function(d){
      //   d.curve((d) => d.linknum)
      // })
      this.links
          // .curve((d) => d.linknum)
          .attr("x1", (d) => {
            return d.source.x;
          })
          .attr("y1", (d) => {
            return d.source.y;
          })
          .attr("x2", (d) => {
            return d.target.x;
          })
          .attr("y2", (d) => {
            return d.target.y;
          });

      this.linksText
          .attr("x", (d) => {
            return (d.source.x + d.target.x) / 2;
          })
          .attr("y", (d) => {
            return (d.source.y + d.target.y) / 2;
          });

      this.gs.attr("transform", (d) => {
        return "translate(" + d.x + "," + d.y + ")";
      });
    },
  },
};
</script>
<style>
.line-text {
  font-size: 0.6rem;
  font-weight: bold;
  fill: #9a9aa2;
  fill-opacity: 1;
  text-anchor: middle;
}

.circle {
  outline-color: orange;
  outline-width: 1rem;
  stroke: #ffd000;
  stroke-width: 1px;
}
</style>
