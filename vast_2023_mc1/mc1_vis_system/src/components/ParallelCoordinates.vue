<template>
  <div class="card flex justify-content-center">
    <div class="p-float-label">
      <Dropdown
          v-model="currentType"
          inputId="dd-type"
          :options="
              nodeTypes.flatMap((e) => {
                return { name: e, code: e };
              })
            "
          optionLabel="name"
          placeholder="Select a Node Type"
          class="w-full md:w-14rem">
        <template #option="slotProps">
          <div class="flex align-items-center">
            <img
                :src="`node/${slotProps.option.name}.svg`"
                style="width: 1rem; height: 1rem"
            />
            <span style="font-size: 1rem; margin-left: 0.5rem">{{
                slotProps.option.name
              }}</span>
          </div>
        </template>
        </Dropdown>
      <label for="dd-type">Select a Node Type</label>
    </div>
  </div>
<!--  <ParallelTest v-show="show('organization')"></ParallelTest>-->
  <div v-if="parallelData">
    <div v-for="type in nodeTypes">
      <ParallelAxis :data="parallelData[type]" :nodeID="nodeID_upon_submit" :anomalies="props.anomalies" v-show="show(type)"/>
    </div>
  </div>
</template>

<script setup>
import {defineProps, ref, toRefs} from "vue";
import Dropdown from "primevue/dropdown";
import ParallelAxis from "./charts/ParallelAxis.vue";
import * as d3 from "d3";

const currentType = ref("null");//现在选中的tab对应的type
//而我们想要它的默认值就是父组件传来的nodeType

let nodeTypes = [
  "person",
  "company",
  "organization",
  "political_organization",
  "vessel",
  "location",
  "event",
  "movement",
  "null",
];
function show(type){
  if (currentType===undefined){
    return false
  } else {
    return currentType.value.name === type;
  }
}

let parallelData;
d3.json("parallelData2.json").then((data) => {
  parallelData = data
})

const props = defineProps({
  //子组件接收父组件传递过来的值
  nodeID: String,
  nodeType: String,
  anomalies: Array
})
console.log(props)
const {nodeID}= toRefs(props)
const {nodeType}= toRefs(props)
const nodeID_upon_submit = ref("Oceanfront Oasis Inc Carriers")
console.log(currentType.value)

function updateAxis(){
  // console.log("updateAxis")
  console.log(nodeID.value)
  nodeID_upon_submit.value = nodeID.value
  // console.log(nodeID_upon_submit.value)
}
defineExpose({updateAxis})
</script>
