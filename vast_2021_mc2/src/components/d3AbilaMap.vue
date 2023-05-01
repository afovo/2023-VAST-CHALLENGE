<template>
  <div id="map">
    <svg></svg>
    <img :src="imgUrl" alt="" style="position:absolute; width:100%; height: 100%; z-index: 0; opacity: 30%; overflow: hidden">
  </div>
</template>

<script>
import * as d3 from "d3";
import abila from "../assets/Abila.json"
import imgUrl from "../assets/MC2-tourist.jpg"
export default {
  name: "d3AbilaMap",
  props: {
    pathCoordsToSend: Map,//需要渲染的路径
    colorMap:Map,
    rangeToAbilia: String
  },
  data () {
    return {
      imgUrl:imgUrl ,
      width: 0,
      height: 0,
      mapContainer: null,
      svg: null,
      zoomHandler: null,
      projection: null,
    }
  },
  mounted() {
    this.width = window.innerWidth;
    this.height = window.innerHeight;
    //定义地图投影
    this.projection=d3.geoMercator()
    this.projection.fitExtent([
      [-this.width*0.14, -this.height*0.005],
      [this.width*0.81, this.height*0.81]
    ], abila);

    console.log(abila);
    //创建svg
    this.svg = d3.select("svg")
        .attr("width", this.width)
        .attr("height", this.height);
    const path = d3.geoPath(this.projection);

    //参考：https://juejin.cn/post/7088501703162462245
    path(abila);
    this.mapContainer = this.svg.append("g");
    this.mapContainer.append('path')
        .datum(abila)
        .attr('d', path)
        // .on("mouseover", function(){
        //   d3.select(this)
        //       .style('stroke','#abc8FF')
        //       .attr('opacity', 1);
        // })
        // .on('mouseout',function(){
        //   d3.select(this)
        //       .style('stroke', '#A5B1D2')
        //       .attr('opacity', 1)
        // })
        .attr("fill", "lightgrey")
        .attr('opacity', 1)
        .attr('stroke', '#A5B1D2')
        .attr('stroke-width', function () {
          return 3
        })
        .attr('transform', "scale(1.2,1)")
    ;
    this.addRect(4,440,85,70,'red',"Abila Airport")
    this.addRect(361,32,85,50,'darkblue',"Desafio Golf Course")
    this.addRect(545,181,85,50,'darkblue',"Ahaggo Museum")
    //ToDo: Tag Other locations

    // this.addZoomBehavior(); // 取消注释，可以拖拽放大地图
    // document.addEventListener('click',function (e) {
    //   console.log(e.clientX)
    //   console.log(e.clientY);
    // });

    //appendix:
    //d3 学习笔记：  https://juejin.cn/user/4485631602599495/posts
    //d3地图缩放平移： https://juejin.cn/post/6844904021027733511
    //Geojson选择生成器： http://geojson.io/#map=4.12/33.34/105.67
    //html 颜色选择器： https://www.w3schools.cn/colors/colors_picker.asp
  },
  methods: {
    addPathDot(x, y, name, color){ //把一个坐标点标注出来
      var pro = this.projection([x,y]);
      var label = this.svg
          .append("g")
          .append("text")
          .attr("x", x)
          .attr("y", y-3)
          .style('font-weight', 400)
          .style('font-family', 'bold')
          .style('fill', color)
          .style('opacity',0)
          .text(name);
      this.mapContainer.append("circle")
          .attr("class","point")
          .attr("cx",pro[0])
          .attr("cy",pro[1])
          .attr("r",5)
          .attr('transform', "scale(1.2,1)")
          .style('fill', color)
          .on("mouseover", function(){
            label.style('opacity',1)
          })
          .on('mouseout', function(){
            label.style('opacity', 0)
          })
      ;
    },
    addRect(x, y, width, height, color, name){
      var label = this.svg
          .append("g")
          .append("text")
          .attr("x", x)
          .attr("y", y-3)
          .style('font-weight', 400)
          .style('font-family', 'bold')
          .style('fill', color)
          .style('opacity',0)
          .text(name);
      this.mapContainer.append("rect")
          .attr('x', x)
          .attr('y', y)
          .attr('width', width)
          .attr('height', height)
          .style('fill', color)
          .style('opacity',0.3)
          .on('mouseover', function(){
            label.style('opacity',1)
          })
          .on('mouseout', function(){
            label.style('opacity', 0)
          })
    },
    addZoomBehavior(){
      this.zoomHandler = d3.zoom()
          .scaleExtent([0.1, 10]) // zoom limit
          .translateExtent([[-100, -100], [this.width + 90, this.height + 100]]) // translate limit
          .on('zoom', ({transform}) => {
            this.mapContainer.attr('transform', transform)
            d3.select("img").attr('transform', transform)
          })
      d3.select("#map").call(this.zoomHandler)
    },
    //参考：https://www.cnblogs.com/ellen-mylife/p/12022299.html#%E5%81%9A%E9%BC%A0%E6%A0%87%E6%96%87%E5%AD%97%E8%B7%9F%E9%9A%8F
    //获取鼠标位置
    mouseXY(e){
      var e1=e||window.event;
      return { "x": e1.offsetX, "y": e1.offsetY };
    },
  },
  watch: {//监听器，数据一旦改变就重新调用
    pathCoordsToSend(pathCoordsToSend){
      if(typeof pathCoordsToSend !== "undefined"){
        if(this.rangeH!==""){
          let p = Object.values(Object.fromEntries(this.pathCoordsToSend));
          let r = p.filter(path => path[0].range_hour===this.rangeH);
          console.log("rangeToAbilia in map", r);
          let all_path = new Map();
          r.forEach( arr=> {
            all_path.set(arr[0].PathId, arr);
          })
          console.log("path to send", all_path)
          all_path.forEach((value, key) => {//key: pathID   value[0]: labels  value[1]:coordinates
            console.log(this.colorMap[key])//ToDo: 这里的颜色不知道为啥是undefined呜呜呜呜呜呜呜
            let name = "CarID: "+value[0]["CarID"] + "Employer: "+value[0]["Employer"]
            value[1].forEach(coor => {
              this.addPathDot(coor[1],coor[0],name,this.colorMap[key])
            })
          })
        }
        else{
          this.disp = Object.fromEntries(pathCoordsToSend);
          console.log("2DCP", pathCoordsToSend);
        }
      }else {
        this.disp = {}
      }
    },
    colorMap(colorMap){
      console.log("Color map in map", colorMap);
    },
    rangeToAbilia(rangeToAbilia){
      if(rangeToAbilia) {
        this.rangeH = rangeToAbilia;
        let p = Object.values(Object.fromEntries(this.pathCoordsToSend));
        let r = p.filter(path => path[0].range_hour === rangeToAbilia);
        console.log("rangeToAbilia in map", r);
        let all_path = new Map();
        r.forEach(arr => {
          all_path.set(arr[0].PathId, arr);
        })
        console.log("path to send", all_path)
        //this.pathCoordsToSend = all_path;
        this.disp = Object.fromEntries(all_path);
      }
    }
  },
}
</script>
<style scoped>
svg {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}
#map{
  position: absolute;
  left: 0;
  top: 1%;
  width: 81%;
  height: 81%;
}
</style>
