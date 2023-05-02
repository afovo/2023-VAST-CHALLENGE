<template>
  <div id="app">
    <div class="four_p1">
      <ForceDirectedGraph></ForceDirectedGraph>
    </div>
    <div class="four_p2">
      <BarChartI></BarChartI>
    </div>
    <div class="four_p3">
      <LineChartI></LineChartI>
    </div>
    <div class="four_p4">

    </div>
  </div>
</template>

<script>
import '../assets/global.css'
import ForceDirectedGraph from "@/components/ForceDirectedGraph";
import BarChartI from "@/components/BarChartI.vue";
import LineChartI from "@/components/LineChartI.vue";

export default {
  name: 'App',
  data(){
    return {
    }
  },
  components:{
    LineChartI,

    BarChartI,
    ForceDirectedGraph,
  },
  methods:{
  },
  beforeCreate(){
  },
  created(){
  },
  beforeMount(){
  },
  mounted(){
  }
}
</script>

<style>
html{
  height:100%;
  width: 100%;
}

body{
  background-color: #303243;
  height:100%;
  width: 100%;
}
*{
  margin: 0px;
  padding: 0px;
  box-sizing: border-box;
}
#app{
  width: 100%;
  height:100%;
}

</style>
