<template>
  <el-collapse v-model="activeNames">
    <!-- filter -->
    <el-collapse-item title="Filter" name="Filter">
      <Filter />
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
</script>
