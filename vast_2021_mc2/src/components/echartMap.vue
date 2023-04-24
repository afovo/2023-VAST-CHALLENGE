<template>
  <div class="echart" id="chart1" ref="chart1" :style="{position:'absolute',width: '100%', height: '100%', background_color: '#fff'}"></div>
</template>

<script>
const echarts = require('echarts')
import jsonData from '../assets/Abila.json' //引入josn文件

export default {
  name: 'AreaEchart',
  mounted() {
    this.initChart();
  },
  data() {
    return {
      option: {
        title: {
          text: 'Abila Map' // 标题
        },
        visualMap: { // 左下角选峰值的小插件
          min: 800,
          max: 50000,
          text: ['High', 'Low'],
          realtime: false,
          calculable: true,
          inRange: {
            color: ['lightskyblue', 'yellow', 'orangered']
          }
        },
        tooltip: { // 鼠标放在省块上展示数据
          trigger: 'item',
          formatter: '{b}<br/>'
        },
        series: [ // 地图参数
          {
            name: 'abila', // 对应json文件名
            type: 'map',
            map: 'abila', // 对应json文件名
            label: {
              // show: true
            },
            data: [
              { name: '青海省', value: 20057.34 },
              { name: '辽宁省', value: 15477.48 },
              { name: '黑龙江省', value: 31686.1 },
              { name: '吉林省', value: 6992.6 },
              { name: '河北省', value: 44045.49 },
              { name: '河南省', value: 40689.64 },
              { name: '山东省', value: 37659.78 },
              { name: '陕西省', value: 45180.97 },
              { name: '山西省', value: 55204.26 },
              { name: '江苏省', value: 21900.9 },
              { name: '浙江省', value: 4918.26 },
              { name: '福建省', value: 5881.84 },
              { name: '广东省', value: 4178.01 },
              { name: '海南省', value: 2227.92 },
              { name: '云南省', value: 2180.98 },
              { name: '江西省', value: 9172.94 },
              { name: '湖南省', value: 3368 },
            ]
          }
        ]
      }
    }
  },
  methods: {
    initChart() {
      echarts.registerMap('abila', jsonData)
      const getchart = echarts.init(this.$refs.chart1)
      getchart.setOption(this.option)
      window.onresize = () => {
        getchart.resize()
      }
    }
  }
}
</script>
