<template>
  <div class="three-canvas" ref="threeTarget"></div>
</template>

<script>
import {ThreeEngine} from './js/TEngine'
import {allBaseObject} from './js/AbilaMap'
import {allLights} from './js/TLights'
import {allHelper} from './js/THelper'

export default {
  name: 'abilaMap',
  data() {
    return {
      ThreeEngine: null,
    };
  },
  mounted() {
    this.ThreeEngine = new ThreeEngine(this.$refs.threeTarget)
    this.ThreeEngine.addObject(...allBaseObject)  // 添加基础模型
    this.ThreeEngine.addObject(...allLights)  // 添加光线
    this.ThreeEngine.addObject(...allHelper)   // 添加辅助
  }
}
</script>

<style scoped>
.three-canvas {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: #d6eaff;
}
</style>
