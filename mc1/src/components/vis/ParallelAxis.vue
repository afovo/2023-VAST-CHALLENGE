<template>
  <div ref="main" style="width: 1536px; height: 800px"></div>
</template>

<script setup>
import { defineProps, onMounted, ref, toRefs, watch } from "vue";
import * as echarts from "echarts";

const props = defineProps({
  //子组件接收父组件传递过来的值
  data: Object,
  nodeID: String, //neighbour id
});
const { nodeID } = toRefs(props);
const anomalies = [
  "Mar de la Vida OJSC",
  "979893388",
  "Oceanfront Oasis Inc Carriers",
  "8327",
];
let selected = props.data.hasOwnProperty(nodeID.value)
  ? [props.data[nodeID.value]]
  : [];
let Suspect = anomalies.map((key) => {
  if (key in props.data) {
    return props.data[key];
  }
  // 设置默认值或者返回 null、undefined 等
  return null;
});

//使用父组件传递过来的值
const data = Object.values(props.data); //这个是不会变的
const avg = [props.data["AVG"]];
const threshold = [props.data["Threshold1"], props.data["Threshold2"]]
let legend = threshold[0]!==undefined?["Normal", "Selected", "Suspect", "Average", "Threshold"]:["Normal", "Selected", "Suspect", "Average"]
console.log(threshold)
const main = ref();

let myChart = null;
const schema = [
  { name: "out degree", index: 0, text: "out\ndegree" },
  { name: "in degree", index: 1, text: "in\ndegree" },
  { name: "1st neighbour person", index: 2, text: "person" },
  { name: "1st neighbour organization", index: 3, text: "organization" },
  { name: "1st neighbour company", index: 4, text: "company" },
  {
    name: "1st neighbour political_organization",
    index: 5,
    text: "political_organization",
  },
  { name: "1st neighbour location", index: 6, text: "location" },
  { name: "1st neighbour vessel", index: 7, text: "vessel" },
  { name: "1st neighbour event", index: 8, text: "event" },
  { name: "1st neighbour movement", index: 9, text: "movement" },
  { name: "1st neighbour null", index: 10, text: "null" },

  { name: "1st neighbour in membership", index: 11, text: "membership" },
  { name: "1st neighbour in partnership", index: 12, text: "partnership" },
  { name: "1st neighbour in ownership", index: 13, text: "ownership" },
  {
    name: "1st neighbour in family_relationship",
    index: 14,
    text: "family\nrelationship",
  },
  { name: "1st neighbour in null", index: 15, text: "null" },
  { name: "1st neighbour out membership", index: 16, text: "membership" },
  { name: "1st neighbour out partnership", index: 17, text: "partnership" },
  { name: "1st neighbour out ownership", index: 18, text: "ownership" },
  {
    name: "1st neighbour out family_relationship",
    index: 19,
    text: "family\nrelationship",
  },
  { name: "1st neighbour out null", index: 20, text: "null" },

  { name: "between neighbour membership", index: 21, text: "membership" },
  { name: "between neighbour partnership", index: 22, text: "partnership" },
  { name: "between neighbour ownership", index: 23, text: "ownership" },
  {
    name: "between neighbour family_relationship",
    index: 24,
    text: "family\nrelationship",
  },
  { name: "between neighbour null", index: 25, text: "null" },

  { name: "in avg weight", index: 26, text: "in avg\n weight" },
  { name: "out avg weight", index: 27, text: "out avg\n weight" },
  { name: "nodeid", index: 28, text: "nodeid" },
];
function init() {
  if (myChart !== null) {
    return;
  }
  myChart = echarts.init(main.value);
  myChart.setOption({
    backgroundColor: "#fff",
    legend: {
      bottom: 30,
      data: legend,
      itemGap: 20,
      textStyle: {
        color: "#222",
        fontSize: 14,
      },
    },
    tooltip: {
      padding: 10,
      backgroundColor: "#fff",
      borderColor: "#aaa",
      textStyle: {
        color: "#222", //设置文字颜色
      },
      enterable: true,
      borderWidth: 1,
      formatter: function (params) {
        setTimeout(function () {
          neighborEdge(params.data);
        }, 10);
        return (
          "<h3>" +
          params.data[28] +
          "</h3>" +
          '<div id="tooltipBarId" style="height:350px;width:330px;border-radius:0 0 5px 0;background:#fff"></div>'
        );
      },
    },
    parallelAxis: [
      { dim: 0, name: schema[0].text },
      { dim: 1, name: schema[1].text },
      { dim: 2, name: schema[2].text },
      { dim: 3, name: schema[3].text },
      { dim: 4, name: schema[4].text },
      { dim: 5, name: schema[5].text },
      { dim: 6, name: schema[6].text },
      { dim: 7, name: schema[7].text },
      { dim: 8, name: schema[8].text },
      { dim: 9, name: schema[9].text },
      { dim: 10, name: schema[10].text },
      { dim: 11, name: schema[11].text },
      { dim: 12, name: schema[12].text },
      { dim: 13, name: schema[13].text },
      { dim: 14, name: schema[14].text },
      { dim: 15, name: schema[15].text },
      { dim: 16, name: schema[16].text },
      { dim: 17, name: schema[17].text },
      { dim: 18, name: schema[18].text },
      { dim: 19, name: schema[19].text },
      { dim: 20, name: schema[20].text },
      { dim: 21, name: schema[21].text },
      { dim: 22, name: schema[22].text },
      { dim: 23, name: schema[23].text },
      { dim: 24, name: schema[24].text },
      { dim: 25, name: schema[25].text },
      { dim: 26, name: schema[26].text },
      { dim: 27, name: schema[27].text },
    ],
    parallel: {
      left: "5%",
      right: "7%",
      bottom: 100,
      parallelAxisDefault: {
        type: "value",
        nameLocation: "end",
        nameGap: 20,
        nameTextStyle: {
          color: "#222",
          fontSize: 8,
        },
        axisLine: {
          lineStyle: {
            color: "#aaa",
          },
        },
        axisTick: {
          lineStyle: {
            color: "#777",
          },
        },
        splitLine: {
          show: false,
        },
        axisLabel: {
          color: "#777",
            fontSize: 8,
        },
      },
    },
    series: [
      {
        name: "Normal",
        type: "parallel",
        coordinateSystem: "parallel",
        data: data,
        lineStyle: {
          width: 1,
          color:"#A3B4CB"
        },
        z: 0,
      },
      {
        name: "Suspect",
        type: "parallel",
        coordinateSystem: "parallel",
        data: Suspect,
        lineStyle: {
          width: 3,
          color: "red",
        },
        z: 1,
      },
      {
        name: "Selected",
        type: "parallel",
        coordinateSystem: "parallel",
        data: selected,
        lineStyle: {
           width: 3,
           color: "blue",
           opacity: 1,
        },
        z: 2,
      },
      {
        name: "Average",
        type: "parallel",
        coordinateSystem: "parallel",
        data: avg,
        lineStyle: {
            width: 4,
            color:"#008080"
        },
        z: 3,
      },
      {
        name: "Threshold",
        type: "parallel",
        coordinateSystem: "parallel",
        data: threshold,
        lineStyle: {
            width: 2,
            color:"green",
            type:"dashed"
        },
        z: 3,
      }
    ],
  });
}

function neighborEdge(data) {
  var myChart1 = echarts.init(document.getElementById("tooltipBarId"));
  var option = {
    tooltip: {
      trigger: "item",
      formatter: "{a} <br/>{b}: {c} ({d}%)",
    },
    legend: {
      top: 0,
      data: ["membership", "partnership", "ownership", "family_relationship"],
    },
    series: [
      {
        name: "Between neighbours",
        type: "pie",
        selectedMode: "single",
        radius: [0, "30%"],
        label: {
          show: true,
          formatter: function (params) {
            if (params.dataIndex === 0) return "Between neighbours";
            else return "";
          },
          position: "center",
          emphasis: {
            textStyle: {
              fontSize: "14",
              fontWeight: "bold",
            },
          },
        },
        data:
          data[21] + data[22] + data[23] + data[24] + data[25] > 0
            ? [
                { value: data[21], name: "membership" },
                { value: data[22], name: "partnership" },
                { value: data[23], name: "ownership" },
                { value: data[24], name: "family_relationship" },
                { value: data[25], name: "null" },
              ]
            : [],
      },
      {
        name: "In Degree",
        type: "pie",
        radius: ["45%", "60%"],
        labelLine: {
          show: false,
        },
        label: {
          show: true,
          formatter: function (params) {
            if (params.dataIndex === 0) return "In Degree";
            else return "";
          },
          position: "inner",
          emphasis: {
            textStyle: {
              fontSize: "14",
              fontWeight: "bold",
            },
          },
        },
        data:
          data[11] + data[12] + data[13] + data[14] + data[15] > 0
            ? [
                { value: data[11], name: "membership" },
                { value: data[12], name: "partnership" },
                { value: data[13], name: "ownership", selected: true },
                { value: data[14], name: "family_relationship" },
                { value: data[15], name: "null" },
              ]
            : [],
      },
      {
        name: "Out Degree",
        type: "pie",
        radius: ["80%", "70%"],
        label: {
          show: true,
          formatter: function (params) {
            if (params.dataIndex === 0) return "Out Degree";
            else return "";
          },
          position: "inner",
          emphasis: {
            textStyle: {
              fontSize: "14",
              fontWeight: "bold",
            },
          },
        },
        data:
          data[16] + data[17] + data[18] + data[19] + data[20] > 0
            ? [
                { value: data[16], name: "membership" },
                { value: data[17], name: "partnership" },
                { value: data[18], name: "ownership", selected: true },
                { value: data[19], name: "family_relationship" },
                { value: data[20], name: "null" },
              ]
            : [],
      },
    ],
  };
  myChart1.setOption(option);
}
function updateOption() {
  myChart.setOption({
      series: [
          {
              name: "Normal",
              type: "parallel",
              coordinateSystem: "parallel",
              data: data,
              lineStyle: {
                  width: 1,
                  color:"#A3B4CB"
              },
              z: 0,
          },
          {
              name: "Suspect",
              type: "parallel",
              coordinateSystem: "parallel",
              data: Suspect,
              lineStyle: {
                  width: 3,
                  color: "red",
              },
              z: 1,
          },
          {
              name: "Selected",
              type: "parallel",
              coordinateSystem: "parallel",
              data: selected,
              lineStyle: {
                  width: 3,
                  color: "blue",
                  opacity: 1,
              },
              z: 2,
          },
          {
              name: "Average",
              type: "parallel",
              coordinateSystem: "parallel",
              data: avg,
              lineStyle: {
                  width: 4,
                  color:"#008080"
              },
              z: 3,
          },
          {
              name: "Threshold",
              type: "parallel",
              coordinateSystem: "parallel",
              data: threshold,
              lineStyle: {
                  width: 2,
                  color:"green",
                  type:"dashed"
              },
              z: 3,
          }
      ]
  });
}
onMounted(init);
watch(
  nodeID,
  (newVal, oldVal) => {
    console.log("parallelAxis update");
    selected = props.data.hasOwnProperty(nodeID.value)
      ? [props.data[nodeID.value]]
      : [];
    updateOption();
  },
  {
    deep: true,
  }
);
</script>

<style scoped></style>
