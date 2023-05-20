<template>
  <el-collapse v-model="activeNames">
    <!-- filter -->
    <el-collapse-item title="Filter" name="Filter">
      <Filter />
    </el-collapse-item>
    <!-- ego net demo -->
    <el-collapse-item title="EgoNet" name="EgoNet">
      <EgoNet />
    </el-collapse-item>
  </el-collapse>
</template>
<style scoped></style>
<script setup>
import EgoNet from "./components/ego.vue";
import Filter from "./components/filter.vue";

let activeNames = $ref(["Filter", "EgoNet"]);
</script>
