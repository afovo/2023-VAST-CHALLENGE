<template>
  <h1>我国人口受教育程度-饼图</h1>
  <div id="arcPie-container"></div>
</template>

<script>
import { defineComponent } from 'vue';
import data from '@/assets/Abila.json';
//import axios from "axios";
import * as d3 from "d3";

// var dataset = [["小学及以下",19.3],["初中",40.3],["高中/中专/技校",20.6],
//   ["大学专科",10.5],["大学本科及以上",9.3]];
console.log(data);
var color=d3.schemeCategory10;

export default defineComponent({
  mounted() {
    // this.drawArcPie(data);
  },
  methods:{
    drawArcPie(dataset){
      const w = 1200;
      const h = 500;
      var svg=d3.select("#arcPie-container")
          .append("svg")
          .attr("width", w)
          .attr("height",h);

      var pie = d3.pie()
          .value(function(d){
            return d[1];
          });
      var piedata = pie(dataset);

      var inner = 50;
      var arc = d3.arc()
          .innerRadius(inner)
          .outerRadius(function(d) {
            var value = d.value;
            return value*4 + inner;
          });

      var arcs = svg.selectAll("g")
          .data(piedata)
          .enter()
          .append("g")
          .attr("transform","translate("+(w/2)+","+(h/2+50)+")");

      arcs.append("path")
          .attr("d",function(d){
            return arc(d);
          })
          .attr("stroke","black")
          .attr("fill",(d,i)=>color[i]);

      svg.selectAll("text1")
          .data(piedata)
          .enter()
          .append("text")
          .attr("transform",function(d){
            //return "translate("+w/2+","+(h/2+50)+")" + "translate("+arc.centroid(d)+")";
            var x = arc.centroid(d)[0];
            var y = arc.centroid(d)[1];
            return "translate("+(w/2+x)+","+(h/2+50+y)+")";
          })
          .attr("text-anchor","middle")
          .attr("fill","black")
          .attr("font-size","12px")
          .text(function(d){
            //return Math.floor((d.endAngle - d.startAngle)*180/Math.PI) + "°";
            return d.value+"%";
          });

      var hei = [240,265,290,315,340];
      svg.selectAll("c")
          .data(hei)
          .enter()
          .append("circle")
          .attr("cx",980)
          .attr("cy",function(d){
            return d;
          })
          .attr("r",6)
          .attr("fill",function(d,i){
            return color[i];
          });

      svg.selectAll("text2")
          .data(hei)
          .enter()
          .append("text")
          .attr("transform",function(d){
            var x = 1000;
            var y = d+6;
            return "translate("+x+","+y+")";
          })
          .attr("fill","black")
          .attr("font-size","14px")
          .text(function(d,i){return dataset[i][0];});
    },
  }
})
</script>
