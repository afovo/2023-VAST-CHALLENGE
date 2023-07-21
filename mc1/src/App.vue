<template>
  <!-- 左边：菜单(filter以及选择不同的图) -->
  <div id="menu">
    <MenuBar ref="MenuBarRef" @getEgoNetFromMenu="getEgoNetFromMenu"></MenuBar>
  </div>
  <!-- 右边：可视化区域 -->
  <div id="vis">
    <router-view v-slot="{ Component }">
      <component ref="ComponentRef" :is="Component" @submit="submit" />
    </router-view>
  </div>
</template>
<script setup>
import {ref, watch, reactive, onMounted} from "vue";
import MenuBar from "./components/menu/MenuBar.vue";
const ComponentRef = ref(null);
const MenuBarRef = ref(null);

const egoid = ref(null)
const egoType = ref(null)
async function getEgoNetFromMenu(net) {
  ComponentRef.value.ComponentName === "ego"
    ? await ComponentRef.value.renderEgoNet(net)
    : {};
    egoid.value = net.ego.id
    egoType.value = net.egoType
}

watch(ComponentRef, (newVal, oldVal) => {
        if (ComponentRef.value){
            if (ComponentRef.value.ComponentName === "parallel"){
                ComponentRef.value.updateAxis(egoid,egoType)
            } else if (ComponentRef.value.ComponentName === "hierarchy"){
                ComponentRef.value.updateNode(egoid)
            }
        }
    },
    {
        deep: true,
    }
)
async function submit(id) {
  await MenuBarRef.value.submit(id);
}

setTimeout(async () => {
  submit("Oceanfront Oasis Inc Carriers");
}, 1);
</script>
