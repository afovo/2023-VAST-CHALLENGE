<template>
  <el-collapse v-model="activeNames">
    <!-- filter -->
    <el-collapse-item title="Filter" name="Filter">
      <Filter :cnt="cnt" />
    </el-collapse-item>
    <!-- d3 net demo -->
    <el-collapse-item title="netVdemo" name="netVdemo">
      <d3MultiForce :data="{nodes:[{id:1,type:1},{id:2,type:2}],links:[{start:1, target:2}]}"></d3MultiForce>
<!--      <netVdemo />-->
    </el-collapse-item>
  </el-collapse>
</template>
<style scoped></style>
<script setup>
import d3MultiForce from "./components/d3MultiForce.vue";
import netVdemo from "./components/netVdemo.vue";
import Filter from "./components/filter.vue";

let activeNames = $ref(["Filter", "netVdemo", "d3MultiForce"]);
let cnt = $ref(9);
d3.json
</script>
