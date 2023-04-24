<template>
  <svg>
  </svg>
</template>

<script>
import * as d3 from "d3";
import abila from "../assets/Abila.json"
export default {
  name: "d3AbilaMap",
  data () {
    return {
      width: 0,
      height: 0,
      mapContainer: null,
      svg: null,
      zoomHandler: null,
    }
  },
  mounted() {
    this.width = window.innerWidth;
    this.height = window.innerHeight;
    //定义地图投影
    var projection=d3.geoMercator()
    projection.fitExtent([
      [0, 0],
      [this.width-20, this.height-20]
    ], abila);

    console.log(abila);
    //创建svg
    this.svg = d3.select("svg")
        .attr("width", this.width)
        .attr("height", this.height);
    const path = d3.geoPath(projection);

    // function fangkuangRemove() {
    //   d3.select("#fangkuang1").remove();
    //   d3.select("#fangkuang2").remove();
    // }
    //创建方框和框内文字

    // function createFangkuang(d) {
    //   let XY=this.mouseXY(event);
    //   d3.select('svg').append("rect")
    //       .attr("id", "fangkuang1")
    //       .attr("x", XY.x)
    //       .attr("y",XY.y)
    //       .attr("class","fangkuang")
    //   //创建显示tooltip文本
    //   d3.select('svg').append("text")
    //       .attr("id", "fangkuang2")
    //       .attr("x", XY.x+40)
    //       .attr("y",XY.y+20)
    //       .attr("text-anchor", "middle")
    //       .attr("font-family", "sans-serif")
    //       .attr("font-size", "14px")
    //       .attr("font-weight", "bold")
    //       .attr("fill", "#fff")
    //       .text(d.properties.name);
    // }
    //参考：https://juejin.cn/post/7088501703162462245
    path(abila);
    this.mapContainer = this.svg.append("g");
    this.mapContainer.append('path')
        .datum(abila)
        .attr('d', path)
        .on("mouseover", function(){
          d3.select(this)
              .style('stroke','#abc8FF')
              .attr('opacity', 1);
          // createFangkuang(d);
        })
        .on('mouseout',function(){
          d3.select(this)
              .style('stroke', '#A5B1D2')
              .attr('opacity', 1)
          // fangkuangRemove();
        })
        .attr("fill", "lightgrey")
        .attr('opacity', 1)
        .attr('stroke', '#A5B1D2')
        .attr('stroke-width', function () {
          return 5
        });
    this.addZoomBehavior();
    // document.addEventListener('mousemove',function (e) {
    //   console.log(e.pageY)
    //   console.log(e.pageX);
    // });


    //appendix:
    //d3 学习笔记：  https://juejin.cn/user/4485631602599495/posts
    //d3地图缩放平移： https://juejin.cn/post/6844904021027733511
    //Geojson选择生成器： http://geojson.io/#map=4.12/33.34/105.67
    //html 颜色选择器： https://www.w3schools.cn/colors/colors_picker.asp
  },
  methods: {
    addZoomBehavior(){
      this.zoomHandler = d3.zoom()
          .scaleExtent([0.1, 10]) // zoom limit
          .translateExtent([[-100, -100], [this.width + 90, this.height + 100]]) // translate limit
          .on('zoom', ({transform}) => {
            this.mapContainer.attr('transform', transform)
          })
      this.svg.call(this.zoomHandler)
    },
    //参考：https://www.cnblogs.com/ellen-mylife/p/12022299.html#%E5%81%9A%E9%BC%A0%E6%A0%87%E6%96%87%E5%AD%97%E8%B7%9F%E9%9A%8F
    //获取鼠标位置
    mouseXY(e){
      var e1=e||window.event;
      return { "x": e1.offsetX, "y": e1.offsetY };
    },
  }
}
</script>
<style scoped>
svg {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
}
</style>
