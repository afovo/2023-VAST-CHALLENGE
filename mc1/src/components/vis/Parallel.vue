<template>
  <div class="card">
    <div class="p-float-label">
      <el-select
        v-model="currentType"
        class="m-2"
        placeholder="Select"
        size="large"
      >
        <el-option
          v-for="item in nodeTypes"
          :key="item"
          :label="item"
          :value="nodeValues[item]"
        />
      </el-select>
      <!--            <label for="dd-type">Select a Node Type</label>-->
    </div>
    <div v-if="parallelData">
          <div v-for="type in nodeTypes">
              <ParallelAxis
                      :ref="child"
                      :data="parallelData[type]"
                      :nodeID="nodeID_upon_submit"
                      v-show="show(type)"
              />
          </div>
      </div>
  </div>

</template>
<style scoped>
.p-float-label {
  display: flex;
    margin-top: 20px;
  justify-content: center;
}
.card{
    background-color: white;
    width:100%;
    height:95%
}
</style>
<script setup>
import { defineProps, ref, toRefs, watch } from "vue";
import Dropdown from "primevue/dropdown";
import ParallelAxis from "./ParallelAxis.vue";
import * as d3 from "d3";
import router from "../../router";

const currentType = ref(); //现在选中的tab对应的type
const child = ref();
//而我们想要它的默认值就是父组件传来的nodeType
let nodeTypes = ["unknown", "company", "organization", "person", "location", "political_organization", "vessel", "movement", "event"];
let nodeValues = {
  person: 0,
  company: 1,
  organization: 2,
  political_organization: 3,
  vessel: 4,
  location: 5,
  event: 6,
  movement: 7,
  unknown: 8,
};
function show(type) {
  if (currentType === undefined) {
    return false;
  } else {
    return currentType.value === nodeValues[type];
  }
}

let parallelData;
d3.json("/data/parallelData.json").then((data) => {
  parallelData = data;
});

const nodeID_upon_submit = ref("Oceanfront Oasis Inc Carriers");

function updateAxis(egoID, egoType) {
  console.log("updateAxis");
  console.log(egoID.value);
  console.log(egoType.value)
  nodeID_upon_submit.value = egoID.value;
  currentType.value = nodeValues[egoType.value];
  setTimeout(() => {
    currentType.value = 1;
  }, 100);
  setTimeout(() => {
    currentType.value = nodeValues[egoType.value];
  }, 100);
  console.log(currentType);
}

const ComponentName = ref("parallel");
defineExpose({ updateAxis, ComponentName });
</script>
