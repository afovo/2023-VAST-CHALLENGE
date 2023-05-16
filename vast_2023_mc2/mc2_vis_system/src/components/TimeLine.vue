<template>
  <div class="slider-demo-block">
    <span class="demonstration">TimeLine</span>
    <el-slider v-model="index" :min="0" :max="10" :step="1" :format-tooltip="function(value){return times[value];}" show-stops />
    <el-button-group>
      <el-button :icon="Minus" @click="decrease" />
      <el-button :icon="Plus" @click="increase" />
    </el-button-group>
  </div>
  <div>{{times}}</div>
</template>

<script setup>
import {ref, defineProps, toRefs} from 'vue'
import { Minus, Plus } from '@element-plus/icons-vue'

const props = defineProps({
  times: {
    type: Array,
    default: ["2009-06-04T09:02:00.000Z", "2009-06-04T09:03:00.000Z", "2009-06-04T09:04:00.000Z", "2009-06-04T09:05:00.000Z", "2009-06-04T09:06:00.000Z", "2009-06-04T09:07:00.000Z", "2009-06-04T09:08:00.000Z", "2009-06-04T09:09:00.000Z", "2009-06-04T09:10:00.000Z", "2009-06-04T09:11:00.000Z", "2009-06-04T09:12:00.000Z", "2009-06-04T09:13:00.000Z", "2009-06-04T09:14:00.000Z", "2009-06-04T09:17:00.000Z", "2009-06-04T09:18:00.000Z", "2009-06-04T09:19:00.000Z", "2009-06-04T09:20:00.000Z", "2009-06-04T09:21:00.000Z", "2009-06-04T09:22:00.000Z", "2009-06-04T09:23:00.000Z", "2009-06-04T09:24:00.000Z", "2009-06-04T09:25:00.000Z", "2009-06-04T09:26:00.000Z", "2009-06-04T09:27:00.000Z", "2009-06-04T09:28:00.000Z", "2009-06-04T09:29:00.000Z", "2009-06-04T09:30:00.000Z", "2009-06-04T09:31:00.000Z", "2009-06-04T09:32:00.000Z", "2009-06-04T09:33:00.000Z", "2009-06-04T09:34:00.000Z", "2009-06-04T09:35:00.000Z", "2009-06-04T09:36:00.000Z", "2009-06-04T09:37:00.000Z", "2009-06-04T09:38:00.000Z", "2009-06-04T09:39:00.000Z", "2009-06-04T09:40:00.000Z", "2009-06-04T09:41:00.000Z", "2009-06-04T09:42:00.000Z", "2009-06-04T09:43:00.000Z", "2009-06-04T09:44:00.000Z", "2009-06-04T09:45:00.000Z", "2009-06-04T09:46:00.000Z", "2009-06-04T09:47:00.000Z", "2009-06-04T09:48:00.000Z", "2009-06-04T09:49:00.000Z", "2009-06-04T09:50:00.000Z", "2009-06-04T09:51:00.000Z", "2009-06-04T09:52:00.000Z"]
  },
});

const { times } = toRefs(props);

let time=0;

let index = ref(0);
const increase = () => {
  index.value ++;
  if (index.value >= times.value.length) {
    index.value = times.value.length-1
  }
  // time.value = times.value[index.value]
  // console.log(time.value)
}
const decrease = () => {
  index.value--;
  if (index.value < 0) {
    index.value = 0
  }
  // time.value = times.value[index.value]
}
</script>
<style scoped>
.slider-demo-block {
  position: absolute;
  left: 10%;
  top:5%;
  width: 80%;
}
.slider-demo-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
}
.slider-demo-block .demonstration {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  line-height: 44px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 0;
}
.slider-demo-block .demonstration + .el-slider {
  flex: 0 0 70%;
}
</style>
