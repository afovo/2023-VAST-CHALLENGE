<template>
  <svg></svg>
</template>

<script>
import * as d3 from "d3";
import china from "../assets/china.geo.json"
// import abila from "../assets/Abila.json"
export default {
  name: "d3AbilaMap",
  mounted() {
    var width = 960, height = 700;
    //1.定义投影和生成器
    //定义地图投影
    var projection=d3.geoMercator()
        .center([107,31]) //地图中心位置,107是经度，31是纬度
        .scale(600) //设置缩放量
        .translate([width/2,height/2]); // 设置平移量

    //定义地理路径生成器,使每一个坐标都会先调用此投影,才产生路径值
    var path=d3.geoPath()
        .projection(projection);// 设定投影

    //3.请求china.geo.json数据,添加<path>,每个path用于绘制一个省的路径
    /**
     * 获取鼠标位置
     * @param {Object} e 当前的元素对象
     */
    function mouseXY(e){
      var e1=e||window.event;
      return { "x": e1.offsetX, "y": e1.offsetY };
    }

    /**
     * 删除文字和方框
     */
    function fangkuangRemove()
    {
      d3.select("#fangkuang1").remove();
      d3.select("#fangkuang2").remove();
    }
    /**
     * 创建方框和框内文字
     * @param {Object} svg
     * @param {Object} d
     */
    function createFangkuang(svg)
    {

      let XY=mouseXY(event);
      svg.append("rect")
          .attr("id", "fangkuang1")
          .attr("x", XY.x)
          .attr("y",XY.y)
          .attr("class","fangkuang")
      //创建显示tooltip文本
      // svg.append("text")
      //     .attr("id", "fangkuang2")
      //     .attr("x", XY.x+40)
      //     .attr("y",XY.y+20)
      //     .attr("text-anchor", "middle")
      //     .attr("font-family", "sans-serif")
      //     .attr("font-size", "14px")
      //     .attr("font-weight", "bold")
      //     .attr("fill", "#fff")
      //     .text(d.properties.name);
    }
    //请求china.geo.json
    console.log(china);
    //创建svg
    var svg = d3.select("svg")
        .attr("width", width)
        .attr("height", height);

    var groups=svg.append("g");

    groups.selectAll("path")
        .data(china.features) // 绑定数据
        .enter()
        .append("path")
        .on('mouseover',function(d){
          d3.select(this)
              .style('fill','#2CD8FF');
          console.log('ss');
          createFangkuang(svg,d);
        })
        .on('mousemove',function(d){
          fangkuangRemove();
          createFangkuang(svg,d);
        })
        .on('mouseout',function(){
          d3.select(this)
              .style('fill', '#404466');
          fangkuangRemove();
        })
        .style("fill",'#404466')//填充内部颜色
        .attr("d",path)//使用路径生成器
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
