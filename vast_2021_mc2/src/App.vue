<template>
<!--    <three-abila-map></three-abila-map>-->
<!--    <d3-abila-map></d3-abila-map>-->
<!--  <echart-map></echart-map>-->
  <!--  <d3-china-map></d3-china-map>-->
<!-- <dash-board></dash-board> -->
<ThreeDashBoard></ThreeDashBoard>
</template>

  <script>
  // import threeAbilaMap from "@/components/threeAbilaMap" //threeJS 3D map of abila
  // import d3AbilaMap from "@/components/d3AbilaMap";  //d3 map of abila
  // import echartMap from "@/components/echartMap"; //echart map of abila
  // import d3ChinaMap from "@/components/d3ChinaMap";  //just a china map demo

  // import dashBoard from "@/view/dashBoard";
  import ThreeDashBoard from './view/ThreeDashBoard.vue';

  export default {
    name: 'App',
    components: {
      // threeAbilaMap,
      // d3AbilaMap,
      // echartMap,
      // d3ChinaMap,
      // dashBoard
      ThreeDashBoard
    }
  }
  </script>

  <style>
  </style>
