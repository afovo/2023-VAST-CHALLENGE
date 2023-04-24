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
//appendix：
// threejs+vue极简例子  https://juejin.cn/post/7209852595002032186#heading-20
// threejs中的线  https://segmentfault.com/a/1190000041607875
// threejs+d3比例尺  全球疫情可视化 https://juejin.cn/post/6955717062979715079
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
