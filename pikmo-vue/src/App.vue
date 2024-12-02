<template>
  <NavBar/>
  <RouterView/>
</template>

<script setup>
  import { RouterLink ,RouterView } from 'vue-router';
  import NavBar from './components/Common/NavBar.vue';
  
  
</script>

<style scoped>
 #app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style>