<template>
<!--<chinaMap></chinaMap>-->
  <abila-map></abila-map>
  </template>

  <script>
  // import chinaMap from "@/components/chinaMap"
  import abilaMap from "@/components/abilaMap"
  export default {
    name: 'App',
    components: {
      abilaMap,
      // chinaMap
    }
  }
  </script>

  <style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
  </style>
