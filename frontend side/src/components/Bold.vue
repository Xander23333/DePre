<template>
  <div id="Bold">
    <div class="container">
      <p>{{prec * 100}}%</p>
      <img src="/static/bold.jpg" alt="#">
    </div>
  </div>
</template>

<script>
export default {
  name:"Bold",
  data(){
    return{
      prec:0.63
    }
  },
  mounted:function(){

  }
}
</script>

<style scoped>
#Bold{
  height: calc(100% - 3rem);
  display: flex;
  justify-content: center;
  align-items: center;
}
.container {
  display: flex;

  align-items: center;
}
.container > p{
  font-size: 4rem;
  color: rgb(22, 168, 231);
  margin-right: 5rem;
}
</style>
