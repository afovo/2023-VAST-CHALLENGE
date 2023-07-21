<template>
  <h3 style="margin-left: 20px">Ownership Stream</h3>
  <el-switch
    v-model="inOrOut"
    size="large"
    active-text="Upper"
    inactive-text="Lower"
    style="margin-left: 20px"
  />
  <HierarchyTree ref="Href" />
</template>
<style></style>
<script setup>
import { ref, watch } from "vue";
import HierarchyTree from "./HierarchyTree.vue";
const Href = ref(null);
const inOrOut = ref(false);
const nodeID = ref();
function updateNode(egoID) {
  console.log("update Hierarchy");
    nodeID.value = egoID;
  let fname = inOrOut.value ? "in" : "out";
  Href.value.init(fname, nodeID);
}

watch(inOrOut, (a, b) => {
  let fname = inOrOut.value ? "in" : "out";
  Href.value.init(fname, nodeID);
});

const ComponentName = ref("hierarchy");
defineExpose({ updateNode, ComponentName });
</script>
