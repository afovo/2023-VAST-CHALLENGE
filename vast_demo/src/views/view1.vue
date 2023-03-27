<template>
  <div id="app">
    <div id="four_p1">
      <scatter_chart></scatter_chart>
    </div>
    <div id="four_p2">
      <map_baidu></map_baidu>
    </div>
    <div id="four_p3">
    </div>
    <div id="four_p4">
      <pie_chart1></pie_chart1>
    </div>
  </div>
</template>

<script>
// import * as d3 from 'd3v4'
// import china_map from './components/china_map'
// import radar_chart from "@/components/radar_chart";
import scatter_chart from "@/components/scatter_chart";
import map_baidu from "@/components/map_baidu";
import pie_chart1 from "@/components/pie_chart1";

export default {
  name: 'App',
  data(){
    return {
    }
  },
  components:{
    // china_map,
    // radar_chart,
    scatter_chart,
    pie_chart1,
    map_baidu
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
