<template>
  <div id="app">
    <Navbar @stop="isStart = false"/>
    <keep-alive>
      <router-view :isStart="isStart" :init="init" @start="isStart = true; init = true"/>
    </keep-alive>
  </div>
</template>

<script>
import Navbar from "@/components/NavBar";
export default {
  name: "App",
  components: {
    Navbar
  },
  data() {
    return {
      init: false,
      isStart: false
    };
  }
};
</script>

<style>
@import url("//at.alicdn.com/t/font_629137_9hbpprhexgeewmi.css");
* {
  box-sizing: border-box;
}
html,
body,
#app {
  height: 100%;
}
body {
  margin: 0;
}
</style>
