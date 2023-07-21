<template>
  <el-menu :collapse="isCollapse" :collapse-transition="false" router>
    <el-menu-item index="ego">
      <img :src="'icons/ego.png'" class="icon" />
      <template #title> Ego Net</template>
    </el-menu-item>
    <el-menu-item index="unity">
      <img :src="'icons/unity.png'" class="icon" />
      <template #title>Unity Net</template>
    </el-menu-item>
    <el-menu-item index="hierarchy">
      <img :src="'icons/hierachy.png'" class="icon" />
      <template #title>Hierarchy Tree</template>
    </el-menu-item>
    <el-menu-item index="parallel">
      <img :src="'icons/parallel.png'" class="icon" />
      <template #title>Parallel Coordinate</template>
    </el-menu-item>
  </el-menu>
  <div id="filterArea" v-show="!isCollapse" style="width: 93%; left:3%; top: 25%">
    <Filter @getEgoNetFromFilter="getEgoNetFromFilter" ref="FilterRef" />
  </div>
</template>
<style scoped>
.icon {
  width: 24px;
  height: 24px;
  margin-right: 1rem;
}
.is-active {
  background-color: #5891cb32;
}
#filterArea {
  width: 240px;
  height: 665px;
  position: absolute;
  bottom: 2px;
  z-index: 2;
  border: solid;
  padding: 2.5px;
  margin-left: 1.5px;
  border-width: 1px;
  border-color: rgba(0, 0, 0, 0.3);
  border-radius: 5px;
}
</style>
<script setup>
import router from "../../router";
import Filter from "./Filter.vue";

import { ref, defineEmits, defineExpose, watch } from "vue";
const isCollapse = ref(false);
const FilterRef = ref(null);
const path = ref(router.currentRoute);

watch(path, (oldVal, newVal) => {
  if (oldVal.path == "/ego") {
    isCollapse.value = false;
    document.getElementById("menu").style.width = 250 + "px";
  } else {
    isCollapse.value = true;
    document.getElementById("menu").style.width = 64 + "px";
  }
});

const emit = defineEmits(["getEgoNetFromMenu"]);
function getEgoNetFromFilter(net) {
  emit("getEgoNetFromMenu", net);
}

async function submit(id) {
  await router.push("ego");
  await FilterRef.value.submit(id);
}

defineExpose({ submit });
</script>
