<template>
    <abila-map></abila-map>
<!--    <d3-abila-map></d3-abila-map>-->
  <!--  <d3-china-map></d3-china-map>-->

</template>

  <script>
  import abilaMap from "@/components/abilaMap" //threeJS 3D map of abila
  // import d3AbilaMap from "@/components/d3AbilaMap";  //d3 map of abila
  // import d3ChinaMap from "@/components/d3ChinaMap";  //just a china map demo

  export default {
    name: 'App',
    components: {
      abilaMap,
      // d3AbilaMap,
      // d3ChinaMap
    }
  }
  </script>

  <style>
  </style>
