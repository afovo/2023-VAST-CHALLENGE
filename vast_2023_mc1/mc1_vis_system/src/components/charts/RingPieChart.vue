<template>
  <div ref="main" style="width: 1500px; height: 500px"></div>
</template>

<script setup>
import {defineProps, onMounted, ref, toRefs, watch} from "vue";
import * as echarts from "echarts";

const main = ref()

let myChart;
function init(){
  myChart = echarts.init(main.value);
  myChart.setOption({
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      data: [
        'Direct',
        'Marketing',
        'Search Engine',
        'Email',
        'Union Ads',
        'Video Ads',
        'Baidu',
        'Google',
        'Bing',
        'Others',
      ]
    },
    series: [
      {
        name: 'Access From',
        type: 'pie',
        selectedMode: 'single',
        radius: [0, '30%'],
        label: {
          position: 'inner',
          fontSize: 14
        },
        labelLine: {
          show: false
        },
        data: [
          { value: 1548, name: 'Search Engine' },
          { value: 775, name: 'Direct' },
          { value: 679, name: 'Marketing', selected: true }
        ]
      },
      {
        name: 'Access From',
        type: 'pie',
        radius: ['45%', '60%'],
        label: {
          show: false
        },
        data: [
          { value: 1048, name: 'Baidu' },
          { value: 335, name: 'Direct' },
          { value: 310, name: 'Email' },
          { value: 251, name: 'Google' },
          { value: 234, name: 'Union Ads' },
          { value: 147, name: 'Bing' },
          { value: 135, name: 'Video Ads' },
          { value: 102, name: 'Others' }
        ]
      },
      {
        name: 'Access From',
        type: 'pie',
        radius: ['80%', '70%'],
        label: {
          show: false
        },
        data: [
          { value: 1048, name: 'Baidu' },
          { value: 335, name: 'Direct' },
        ]
      },
    ]
  })
}

onMounted(init)



function updateOption(){
  myChart.setOption(
      {
        series: [
          {
            name: 'Normal',
            type: 'parallel',
            coordinateSystem: 'parallel',
            data: data,
            lineStyle: {
              width: 1
            },
            z:0
          },
          {
            name: 'Anomaly',
            type: 'parallel',
            coordinateSystem: 'parallel',
            data: anomaly,
            lineStyle: {
              width: 5,
              color: "red"
            },
            z:1
          },
          {
            name: 'Selected',
            type: 'parallel',
            coordinateSystem: 'parallel',
            data: selected,
            lineStyle: {
              width: 5,
              color: "blue",
              opacity: 1
            },
            z:2
          },
          {
            name: 'Average',
            type: 'parallel',
            coordinateSystem: 'parallel',
            data: avg,
            lineStyle: {
              width: 3,
            },
            z:3
          },
        ],
      }
  )
}

// watch(nodeID, (newVal, oldVal) => {
//       console.log('parallelAxis update')
//       selected = props.data.hasOwnProperty(nodeID.value)?[props.data[nodeID.value]]:[]
//       updateOption()
//     },
//     {
//       deep: true,
//     }
// )
// watch(anomalies, (newVal, oldVal) => {
//       console.log('parallelAxis update')
//       anomaly = [...anomalies.value].map(key => {
//         if (key in props.data) {
//           return props.data[key];
//         }
//         return null;
//       });
//       updateOption()
//     },
//     {
//       deep: true,
//     }
// )
</script>

<style scoped>

</style>
