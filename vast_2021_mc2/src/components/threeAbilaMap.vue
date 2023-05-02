<template>
  <div class="three-canvas" ref="threeTarget"></div>
</template>

<script>
import { ThreeEngine } from './js/TEngine'
import { allBaseObject } from './js/AbilaMap'
import { allLights } from './js/TLights'
import { allHelper } from './js/THelper'
// import { selectedLines } from './js/TLines'
import * as d3 from "d3";
import {
  LineBasicMaterial,
  BufferGeometry,
  Vector3,
  Line,
  // Color,
  // MeshLambertMaterial,
  // DoubleSide,
  // Mesh
} from "three"
// import { select } from 'd3'

export default {
  name: 'abilaMap',
  props: {
    pathCoordsToSend: Map,//需要渲染的路径
    colorMap:Map,
    // rangeToAbilia: String
  },
  data() {
    return {
      ThreeEngine: null,
     
    };
  },
  mounted() {
    this.ThreeEngine = new ThreeEngine(this.$refs.threeTarget)
    this.ThreeEngine.addObject(...allBaseObject)  // 添加基础模型
    this.ThreeEngine.addObject(...allLights)  // 添加光线
    this.ThreeEngine.addObject(...allHelper)   // 添加辅助
    // this.ThreeEngine.addObject(...selectedLines)
  },
  methods: {


    drawLines(line_info) {
      const geometry = new BufferGeometry();
      var material = new LineBasicMaterial({ color: line_info[0][3] });
      const pointsArray = [];
      let xScale = d3.scaleLinear().domain([20, 30]).range([-1035, 1095]);//地图太小了 比例尺放大
      let yScale = d3.scaleLinear().domain([30, 40]).range([-1290, 840]);
      // let p = Object.values(Object.fromEntries(pathCoord));
      for (let i = 0; i < line_info.length; i++) {
        pointsArray.push(new Vector3(xScale(line_info[i][0]), 0.5, yScale(line_info[i][1])));
      }

      geometry.setFromPoints(pointsArray);
      // console.log(pointsArray[0])

      var line = new Line(geometry, material);
      // allTrackLines.push(line);
      console.log("line", line)
      this.ThreeEngine.addObject(line);
    }
  },
  watch: {//监听器，数据一旦改变就重新调用
    colorMap(colorMap) {
      console.log("Color map in map", colorMap);
    },
    pathCoordsToSend(pathCoordsToSend) {
      if (typeof pathCoordsToSend !== "undefined") {
        if (this.rangeH !== "") {
          let p = Object.values(Object.fromEntries(this.pathCoordsToSend));
          // let r = p.filter(path => path[0].range_hour===this.rangeH);
          // console.log("rangeToAbila in map", r);
          let all_path = new Map();
          p.forEach( arr=> {
            all_path.set(arr[0].PathId, arr);
          })
          // console.log("path to send", all_path)
          // console.log("path coordinates to send", this.pathCoordsToSend.get("98.0"))
          // console.log("color map", this.colorMap.get("1.0"))
          
          all_path.forEach((value, key) => {//key: pathID   value[0]: labels  value[1]:coordinates
            let name = "CarID: " + value[0]["CarID"] + "Employer: " + value[0]["Employer"]
            const lines_points=[]
            value[1].forEach(coor => {
              lines_points.push([coor[1], coor[0], name, this.colorMap.get(key)])
            })
            console.log(lines_points.length)
            this.drawLines(lines_points)
          })
        }
        else {
          this.disp = Object.fromEntries(pathCoordsToSend);
          console.log("2DCP", pathCoordsToSend);
        }
      } else {
        this.disp = {}
      }
    },

    // colorMap(colorMap){
    //   console.log("Color map in map", colorMap);
    // },
    // rangeToAbila(rangeToAbila){
    //   if(rangeToAbila) {
    //     this.rangeH = rangeToAbila;
    //     let p = Object.values(Object.fromEntries(this.pathCoordsToSend));
    //     let r = p.filter(path => path[0].range_hour === rangeToAbila);
    //     console.log("rangeToAbila in map", r);
    //     let all_path = new Map();
    //     r.forEach(arr => {
    //       all_path.set(arr[0].PathId, arr);
    //     })
    //     console.log("path to send", all_path)
    //     //this.pathCoordsToSend = all_path;
    //     this.disp = Object.fromEntries(all_path);
    //   }
    // }
  },

}
//appendix：
// threejs+vue极简例子  https://juejin.cn/post/7209852595002032186#heading-20
// threejs中的线  https://segmentfault.com/a/1190000041607875
// threejs+d3比例尺  全球疫情可视化 https://juejin.cn/post/6955717062979715079
</script>

<style scoped>
.three-canvas {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: #d6eaff;
}
</style>
