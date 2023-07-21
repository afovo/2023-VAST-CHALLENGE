<template>
  <div id="chart" style="width: 600px; height: 400px;"></div>
</template>

<script setup>
import * as echarts from 'echarts';
import {onMounted} from "vue";

const data = [
  [1, 2, 3, 4, 5],
  [2, 4, 6, 8, 10],
  [3, 6, 9, 12, 15]
];

// 设置每条线的ID
const ids = ['A', 'B', 'C'];
const widths = [1,5,10]

onMounted(() => {
// 创建 ECharts 实例
  const chart = echarts.init(document.getElementById('chart'));

// 设置平行坐标系
  chart.setOption({
    tooltip: {
      trigger: 'axis'
    },
    parallelAxis: [
      { dim: 0 },
      { dim: 1 },
      { dim: 2 },
      { dim: 3 },
      { dim: 4 }
    ],
    parallel: {
      parallelAxisDefault: {
        type: 'value'
      }
    },
    series: [
      {
        type: 'parallel',
        coordinateSystem: 'parallel',
        data: data,
        lineStyle: {
          color: function (params) {
            // 根据数据的ID设置线的颜色
            const id = ids[params.dataIndex];
            return idToColor(id);
          },
          width: 5
        }
      }
    ]
  });

  function idToColor(id) {
    if (id === 'A') {
      return 'red';
    } else if (id === 'B') {
      return 'green';
    } else if (id === 'C') {
      return 'blue';
    }
    // 默认颜色
    return 'black';
  }

// 调整图表大小
  window.addEventListener('resize', () => {
    chart.resize();
  });
})
</script>
