<template>
  <div id="pie" :style="{width: '100%', height: '100%'}" />
</template>

<script>
export default {
  mounted() {
    this.drawLine()
  },
  methods: {
    drawLine() {
      // 基于准备好的dom，初始化echarts实例
      const pie = this.$echarts.init(document.getElementById('pie'))
      pie.setOption({
        title: [
          {
            text: '雷达图',
            left:'center'
          }
        ],
        polar: {
          radius: [30, '70%']
        },
        radiusAxis: {
          max: 4
        },
        angleAxis: {
          type: 'category',
          data: ['a', 'b', 'c', 'd'],
          startAngle: 75
        },
        tooltip: {},
        series: {
          type: 'bar',
          data: [2, 1.2, 2.4, 3.6],
          coordinateSystem: 'polar',
          label: {
            show: true,
            position: 'middle',
            formatter: '{b}: {c}'
          }
        },
        backgroundColor: '#fff',
        animation: false
      })
    }
  }
}
</script>
