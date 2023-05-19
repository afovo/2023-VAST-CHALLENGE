<template>
  <el-collapse v-model="activeNames">
    <!-- filter -->
    <el-collapse-item title="Filter" name="Filter">
      <Filter :cnt="cnt" />
    </el-collapse-item>
    <!-- d3 net demo -->
    <el-collapse-item title="netVdemo" name="netVdemo">
      <netVdemo />
    </el-collapse-item>
  </el-collapse>
</template>
<style scoped></style>
<script setup>
import netVdemo from "./components/netVdemo.vue";
import Filter from "./components/filter.vue";

let activeNames = $ref(["Filter", "netVdemo"]);
let cnt = $ref(9);
data = {
  1: { 1: {}, 2: 1 },
  2: { 1: 0, 2: 1 },
};
</script>
