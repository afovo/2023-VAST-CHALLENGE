<template>
  <e-charts :option="option"></e-charts>
</template>

<script>
import {defineProps, toRefs} from "vue";
//
const props = defineProps({
  //子组件接收父组件传递过来的值
  inData: Map,
  outData: Map
})
//使用父组件传递过来的值
const {inData} = toRefs(props)
const {outData} = toRefs(props)

export default {
  props: {
    inData: {
      type: Map,
      required: true
    },
    outData: {
      type: Map,
      required: true
    }
  },
  name: "StackedColumnChart",
  setup(props) {
    const {inData, outData} = toRefs(props);
    console.log('aaaaaaaaaaaaaajiuming')
    console.log(inData)
    console.log(outData)
    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {},
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          data: ['membership', 'partnership', 'ownership', 'family_relationship', 'undefined']
        }
      ],
      yAxis: [
        {
          type: 'value'
        }
      ],
      series: [
        {
          name: 'person',
          type: 'bar',
          stack: 'out-degree',
          emphasis: {
            focus: 'series'
          },
          data: outData.value.get("person")
        },
        {
          name: 'organization',
          type: 'bar',
          stack: 'out-degree',
          emphasis: {
            focus: 'series'
          },
          data: outData.value.get("organization")
        },
        {
          name: 'company',
          type: 'bar',
          stack: 'out-degree',
          emphasis: {
            focus: 'series'
          },
          data: outData.value.get("company")
        },
        {
          name: 'political_organization',
          type: 'bar',
          stack: 'out-degree',
          emphasis: {
            focus: 'series'
          },
          data: outData.value.get("political_organization")
        },
        {
          name: 'location',
          type: 'bar',
          stack: 'out-degree',
          data: outData.value.get("location"),
          emphasis: {
            focus: 'series'
          }
        },
        {
          name: 'vessel',
          type: 'bar',
          stack: 'out-degree',
          emphasis: {
            focus: 'series'
          },
          data: outData.value.get("vessel")
        },
        {
          name: 'event',
          type: 'bar',
          stack: 'out-degree',
          emphasis: {
            focus: 'series'
          },
          data: outData.value.get("event")
        },
        {
          name: 'movement',
          type: 'bar',
          stack: 'out-degree',
          emphasis: {
            focus: 'series'
          },
          data: outData.value.get("movement")
        },


        {
          name: 'person',
          type: 'bar',
          stack: 'in-degree',
          emphasis: {
            focus: 'series'
          },
          data: inData.value.get("person")
        },
        {
          name: 'organization',
          type: 'bar',
          stack: 'in-degree',
          emphasis: {
            focus: 'series'
          },
          data: inData.value.get("organization")
        },
        {
          name: 'company',
          type: 'bar',
          stack: 'in-degree',
          emphasis: {
            focus: 'series'
          },
          data: inData.value.get("company")
        },
        {
          name: 'political_organization',
          type: 'bar',
          stack: 'in-degree',
          emphasis: {
            focus: 'series'
          },
          data: inData.value.get("political_organization")
        },
        {
          name: 'location',
          type: 'bar',
          stack: 'in-degree',
          data: inData.value.get("location"),
          emphasis: {
            focus: 'series'
          }
        },
        {
          name: 'vessel',
          type: 'bar',
          stack: 'in-degree',
          emphasis: {
            focus: 'series'
          },
          data: inData.value.get("vessel")
        },
        {
          name: 'event',
          type: 'bar',
          stack: 'in-degree',
          emphasis: {
            focus: 'series'
          },
          data: inData.value.get("event")
        },
        {
          name: 'movement',
          type: 'bar',
          stack: 'in-degree',
          emphasis: {
            focus: 'series'
          },
          data: inData.value.get("movement")
        }

      ]

    };

    return {
      option
    };
  }
  // computed: {
  //   option() {
  //     return {
  //
  //       tooltip: {
  //         trigger: 'axis',
  //         axisPointer: {
  //           type: 'shadow'
  //         }
  //       },
  //       legend: {},
  //       grid: {
  //         left: '3%',
  //         right: '4%',
  //         bottom: '3%',
  //         containLabel: true
  //       },
  //       xAxis: [
  //         {
  //           type: 'category',
  //           data: ['membership', 'partnership', 'ownership', 'family_relationship', 'undefined']
  //         }
  //       ],
  //       yAxis: [
  //         {
  //           type: 'value'
  //         }
  //       ],
  //       series: [
  //         {
  //           name: 'person',
  //           type: 'bar',
  //           stack: 'out-degree',
  //           emphasis: {
  //             focus: 'series'
  //           },
  //           data: outData.
  //         },
  //         {
  //           name: 'organization',
  //           type: 'bar',
  //           stack: 'out-degree',
  //           emphasis: {
  //             focus: 'series'
  //           },
  //           data: [120, 132, 101, 134, 0]
  //         },
  //         {
  //           name: 'company',
  //           type: 'bar',
  //           stack: 'out-degree',
  //           emphasis: {
  //             focus: 'series'
  //           },
  //           data: [220, 182, 191, 234, 0]
  //         },
  //         {
  //           name: 'political_organization',
  //           type: 'bar',
  //           stack: 'out-degree',
  //           emphasis: {
  //             focus: 'series'
  //           },
  //           data: [150, 232, 201, 154, 0]
  //         },
  //         {
  //           name: 'location',
  //           type: 'bar',
  //           stack: 'out-degree',
  //           data: [862, 1018, 964, 1026, 0],
  //           emphasis: {
  //             focus: 'series'
  //           }
  //         },
  //         {
  //           name: 'vessel',
  //           type: 'bar',
  //           stack: 'out-degree',
  //           emphasis: {
  //             focus: 'series'
  //           },
  //           data: [620, 732, 701, 734, 0]
  //         },
  //         {
  //           name: 'event',
  //           type: 'bar',
  //           stack: 'out-degree',
  //           emphasis: {
  //             focus: 'series'
  //           },
  //           data: [120, 132, 101, 134, 0]
  //         },
  //         {
  //           name: 'movement',
  //           type: 'bar',
  //           stack: 'out-degree',
  //           emphasis: {
  //             focus: 'series'
  //           },
  //           data: [60, 72, 71, 74, 0]
  //         },
  //
  //
  //         {
  //           name: 'person',
  //           type: 'bar',
  //           stack: 'in-degree',
  //           emphasis: {
  //             focus: 'series'
  //           },
  //           data: [320, 332, 301, 334, 0]
  //         },
  //         {
  //           name: 'organization',
  //           type: 'bar',
  //           stack: 'in-degree',
  //           emphasis: {
  //             focus: 'series'
  //           },
  //           data: [120, 132, 101, 134, 0]
  //         },
  //         {
  //           name: 'company',
  //           type: 'bar',
  //           stack: 'in-degree',
  //           emphasis: {
  //             focus: 'series'
  //           },
  //           data: [220, 182, 191, 234, 0]
  //         },
  //         {
  //           name: 'political_organization',
  //           type: 'bar',
  //           stack: 'in-degree',
  //           emphasis: {
  //             focus: 'series'
  //           },
  //           data: [150, 232, 201, 154, 0]
  //         },
  //         {
  //           name: 'location',
  //           type: 'bar',
  //           stack: 'in-degree',
  //           data: [862, 1018, 964, 1026, 0],
  //           emphasis: {
  //             focus: 'series'
  //           }
  //         },
  //         {
  //           name: 'vessel',
  //           type: 'bar',
  //           stack: 'in-degree',
  //           emphasis: {
  //             focus: 'series'
  //           },
  //           data: [620, 732, 701, 734, 0]
  //         },
  //         {
  //           name: 'event',
  //           type: 'bar',
  //           stack: 'in-degree',
  //           emphasis: {
  //             focus: 'series'
  //           },
  //           data: [120, 132, 101, 134, 0]
  //         },
  //         {
  //           name: 'movement',
  //           type: 'bar',
  //           stack: 'in-degree',
  //           emphasis: {
  //             focus: 'series'
  //           },
  //           data: [60, 72, 71, 74, 0]
  //         }
  //
  //       ]
  //
  //     }
  //   }
  // }
}
</script>

<style scoped>

</style>