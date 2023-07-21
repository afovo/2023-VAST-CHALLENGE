<template>
  <div ref="main" style="width: 1000px; height: 500px"></div>
</template>

<script setup>
import {defineProps, ref, toRefs, watch} from "vue";
import * as echarts from "echarts";
import * as d3 from "d3";
import {color} from "echarts";
let anomaly = ["Mar de la Vida OJSC",
      "979893388",
      "Oceanfront Oasis Inc Carriers",
      "8327"]
//
let colors = ["#50a3ba","#AFEEEE","#DDA0DD","#FFE4E1",
  "#F5DEB3","#98FB98","#FFA07A","#8FBC8F",
  "#7B68EE"]
function idToColor(id, seq){
  if(id==="12744"){//nodeID.value
    return "red"
  } else if(anomaly.includes(id)){
    return "blue"
  } else {
    return colors[seq]
  }
}
const props = defineProps({
  //子组件接收父组件传递过来的值
  nodeID: String, //neighbour id
})
//使用父组件传递过来的值
const {nodeID} = toRefs(props)
const main = ref()

let myChart = null;

let person = [];
let organization = [];
let company = [];
let political_organization = [];
let location = [];
let vessel = [];
let event = [];
let movement = [];
let unknown = [];

/*
0：出度/总边数  1,2，3，4，5，6, 7, 8, 9一阶邻居节点类型分布，
    #                                            # 10,11，12，13，14一阶入边类型分布
    #                                            # 15,16，17，18，19一阶出边类型分布
    #                                            # 20,21，22，23，24一阶之间连边的类型分布
    #                                              25  入边平均权重
    #                                              26  出边平均权重
    #                                              27  name
 */
//"person","organization","company","political_organization","location","vessel","event", "movement", "null"
//edge_type_mapping = {"membership": 0, "partnership": 1, "ownership": 2, "family_relationship": 3, None: 4}
var schema = [
  { name: 'out degree/all', index: 0, text: 'outD/all' },
  { name: '1st neighbour person', index: 1, text: 'person' },
  { name: '1st neighbour organization', index: 2, text: 'organization' },
  { name: '1st neighbour company', index: 3, text: 'company' },
  { name: '1st neighbour political_organization', index: 4, text: 'political_organization' },
  { name: '1st neighbour location', index: 5, text: 'location' },
  { name: '1st neighbour vessel', index: 6, text: 'vessel' },
  { name: '1st neighbour event', index: 7, text: 'event' },
  { name: '1st neighbour movement', index: 8, text: 'movement' },
  { name: '1st neighbour null', index: 9, text: 'null' },

  { name: '1st neighbour in membership', index: 10, text: 'membership' },
  { name: '1st neighbour in partnership', index: 11, text: 'partnership' },
  { name: '1st neighbour in ownership', index: 12, text: 'ownership' },
  { name: '1st neighbour in family_relationship', index: 13, text: 'family_relationship' },
  { name: '1st neighbour in null', index: 14, text: 'null' },
  { name: '1st neighbour out membership', index: 15, text: 'membership' },
  { name: '1st neighbour out partnership', index: 16, text: 'partnership' },
  { name: '1st neighbour out ownership', index: 17, text: 'ownership' },
  { name: '1st neighbour out family_relationship', index: 18, text: 'family_relationship' },
  { name: '1st neighbour out null', index: 19, text: 'null' },

  { name: 'between neighbour membership', index: 20, text: 'membership' },
  { name: 'between neighbour partnership', index: 21, text: 'partnership' },
  { name: 'between neighbour ownership', index: 22, text: 'ownership' },
  { name: 'between neighbour family_relationship', index: 23, text: 'family_relationship' },
  { name: 'between neighbour null', index: 24, text: 'null' },

  { name: 'in avg weight', index: 25, text: 'in avg weight' },
  { name: 'out avg weight', index: 26, text: 'out avg weight' },
  { name: 'nodeid', index: 27, text: 'nodeid' },
];

d3.json("parallelData.json").then((data) => {
  person = data['person']
  organization = data['organization']
  organization.push(organization.splice(0, 1)[0]);
  company = data['company']
  political_organization = data['political_organization'];
  location = data['location'];
  vessel = data['vessel'];
  event = data['event'];
  movement = data['movement'];
  unknown = data['unknown'];
})
function updateOption(){
  myChart = echarts.init(main.value);
  myChart.setOption({
    backgroundColor: '#333',
    color: colors,
    legend: {
      bottom: 30,
      data: ["person","organization","company","political_organization","location","vessel","event", "movement", "unknown"],
      itemGap: 20,
      textStyle: {
        color: '#fff',
        fontSize: 14
      }
    },
    tooltip: {
      padding: 10,
      backgroundColor: '#222',
      borderColor: '#777',
      borderWidth: 1
    },
    parallelAxis: [
      {
        dim: 0,
        name: schema[0].text,
        max: 1,
        // nameLocation: 'start'
      },
      { dim: 1, name: schema[1].text, max: 1},
      { dim: 2, name: schema[2].text, max: 1},
      { dim: 3, name: schema[3].text, max: 1},
      { dim: 4, name: schema[4].text, max: 1},
      { dim: 5, name: schema[5].text, max: 1},
      { dim: 6, name: schema[6].text, max: 1},
      { dim: 7, name: schema[7].text, max: 1},
      { dim: 8, name: schema[8].text, max: 1},
      { dim: 9, name: schema[9].text, max: 1},
      { dim: 10, name: schema[10].text, max: 1},
      { dim: 11, name: schema[11].text, max: 1},
      { dim: 12, name: schema[12].text, max: 1},
      { dim: 13, name: schema[13].text, max: 1},
      { dim: 14, name: schema[14].text, max: 1},
      { dim: 15, name: schema[15].text, max: 1},
      { dim: 16, name: schema[16].text, max: 1},
      { dim: 17, name: schema[17].text, max: 1},
      { dim: 18, name: schema[18].text, max: 1},
      { dim: 19, name: schema[19].text, max: 1},
      { dim: 20, name: schema[20].text, max: 1},
      { dim: 21, name: schema[21].text, max: 1},
      { dim: 22, name: schema[22].text, max: 1},
      { dim: 23, name: schema[23].text, max: 1},
      { dim: 24, name: schema[24].text, max: 1},
      { dim: 25, name: schema[25].text, max: 1},
      { dim: 26, name: schema[26].text, max: 1},
      { dim: 27, name: schema[27].text}
    ],
    // visualMap: {
    //   show: true,
    //   min: 0,
    //   max: 150,
    //   dimension: 2,
    //   inRange: {
    //     color: ['#d94e5d', '#eac736', '#50a3ba'].reverse()
    //     // colorAlpha: [0, 1]
    //   }
    // },
    parallel: {
      left: '5%',
      right: '18%',
      bottom: 100,
      parallelAxisDefault: {
        type: 'value',
        nameLocation: 'end',
        nameGap: 20,
        nameTextStyle: {
          color: '#fff',
          fontSize: 12
        },
        axisLine: {
          lineStyle: {
            color: '#aaa'
          }
        },
        axisTick: {
          lineStyle: {
            color: '#777'
          }
        },
        splitLine: {
          show: false
        },
        axisLabel: {
          color: '#fff'
        }
      }
    },
    //"person","organization","company","political_organization","location","vessel","event", "movement", "unknown"
    series: [
      {
        name: 'person',
        type: 'parallel',
        coordinateSystem: 'parallel',
        data: person
      },
      {
        name: 'organization',
        type: 'parallel',
        coordinateSystem: 'parallel',
        data: organization,
        lineStyle: {
          width: 2,
          opacity: (params)=>{return anomaly.includes(params.data[27])?1:0.1},
          //     function (params) {
          //   return 5
          //   console.log("??????????????")
          //   console.log(nodeID.value)
          //   if (anomaly.includes(params.data[27])||params.data[27]===nodeID.value) {
          //     console.log(params.data[27])
          //     return 5
          //   } else {
          //     return 1
          //   }
          //   return anomaly.includes(params.data[27])||params.data[27]===nodeID.value?5:1;
          // },
          color: function (params) {
            return idToColor(params.data[27], 1);
          },
        },
        emphasis: {
          focus: 'series', // 设置 focus 为 'series'
          lineStyle: {
            width: 3, // 突出显示的线条宽度,
            z:100
          }
        }
      },

      {
        name: 'company',
        type: 'parallel',
        coordinateSystem: 'parallel',
        data: company
      },
      {
        name: 'political_organization',
        type: 'parallel',
        coordinateSystem: 'parallel',
        data: political_organization
      },
      {
        name: 'location',
        type: 'parallel',
        coordinateSystem: 'parallel',
        data: location
      },
      {
        name: 'vessel',
        type: 'parallel',
        coordinateSystem: 'parallel',
        data: vessel
      },
      {
        name: 'event',
        type: 'parallel',
        coordinateSystem: 'parallel',
        data: event
      },
      {
        name: 'movement',
        type: 'parallel',
        coordinateSystem: 'parallel',
        data: movement
      },
      {
        name: 'unknown',
        type: 'parallel',
        coordinateSystem: 'parallel',
        data: unknown,
        lineStyle: function (params) {
            return idToColor(params.data[27], 8);
        }
      },
    ],

  })
}

watch(() =>(nodeID),
    (newVal, oldVal) => {
      console.log('parallelAxis update')
      updateOption()
    },
    {
      deep: true,
    }
)

let lineStyles = [
  {
    width: 1,
    opacity: 0.5,
    color: "#50a3ba"
    // color: "#FF5252"
  },
  {
    width: 10,
    opacity: 0.5,
    color: "#FFFFFF"
    // color: "#FF5252"
  },
  {
    width: 5,
    opacity: 0.5,
    color: "#FF5252"
    // color: "#FF5252"
  }

];

</script>

<style scoped>

</style>
