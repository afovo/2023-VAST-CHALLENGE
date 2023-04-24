<template>
  <svg></svg>
</template>

<script>
import * as d3 from "d3";
import abila from "../assets/Abila1.json"//和abila.json的区别是去掉了所有null值
export default {
  name: "d3AbilaMap",
  mounted() {
    var width = window.innerWidth, height = window.innerHeight;
    // let scaler = d3.scaleLinear().domain([20,30]).range([-1035,1095]);
    //定义地图投影
    var projection=d3.geoTransverseMercator().fitExtent(
        [
          [24.82403, 36.045015],
          [24.909965, 36.094918],
        ], abila).scale(100000000)
        // .center([24.866294131254598, 36.06480338619151]) //地图中心位置
        // .scale(100) //设置缩放量
        // .translate([width*2,height*2]); // 设置平移量

    console.log(abila);
    //创建svg
    var svg = d3.select("svg")
        .attr("width", width)
        .attr("height", height);
    const path = d3.geoPath(projection);

    //参考：https://juejin.cn/post/7088501703162462245
    //用这下边这两个生成path都十分正常
    // const collection = {
    //   "type": "FeatureCollection",
    //   "features": [{
    //     type: "Feature",
    //     properties: {},
    //     // Point: 点
    //     geometry: {
    //       type:"LineString",
    //       coordinates:[[18,18],[24.841563,36.07042]],
    //     }},
    //     {
    //       type: "Feature",
    //       properties: {},
    //       // Point: 点
    //       geometry: {
    //         type: "Point",
    //         coordinates: [25, 30],
    //       }
    //     }]
    // }

    // const point = {
    //       type: "Feature",
    //       properties: {},
    //       // Point: 点
    //       geometry: {
    //         type: "Point",
    //         coordinates: [20, 30],
    //       },
    // };

    //但是用去了null的json它就看不见了、
    //尝试改json数据，比如一边端点24.xx,38.xx改成2400.xx, 38.xx会出来一条线
    // 怀疑是projection的scale有问题，但是调了半天都不行
    path(
        abila
    )
    svg.append('path')
        .datum(abila)
        .attr('d', path);
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
