<template>
  <div id="app">
    <div class="four_p1">
      <ForceDirectedGraph></ForceDirectedGraph>
    </div>
    <div class="four_p2">

    </div>
    <div class="four_p3">
    </div>
    <div class="four_p4">

    </div>
  </div>
</template>

<script>
import '../assets/global.css'
import ForceDirectedGraph from "@/components/ForceDirectedGraph";
export default {
  name: 'App',
  data(){
    return {
    }
  },
  components:{
    ForceDirectedGraph
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
