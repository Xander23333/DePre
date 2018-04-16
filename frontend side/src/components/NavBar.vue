<template>
  <div id="Navbar">
    <p id="title">KYShooter</p>
    <ul id="nav-link">
      <router-link to="/">Shooter</router-link>
      <router-link to="/Dashboard">Bigger Shooter</router-link>
      <router-link to="/bold">Blod</router-link>
    </ul>
    <button @click="$emit('stop')">stop</button>
  </div>
</template>

<script>
export default {
  name:'Navbar'
}
</script>

<style scoped>
#Navbar{
  height: 3rem;
  width: 100%;
  background-color: white;
  border-bottom: 1px solid rgba(0, 0, 0, 0.25);
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.25);
  display: flex;
  align-content: center;
}

#title{
  font-size: 2rem;
  font-weight: 1.5;
  color: #333;
  line-height: 3rem;
  margin: 0;
  margin-left: 1rem;
  margin-right: auto;
}

#nav-link{
  float: left;
  margin:1rem;
  list-style: none;
}
#nav-link > a{
  color:white;
  text-align: center;
  text-decoration: none;
  background-color: rgb(63, 177, 227);
  border-radius: 3px;
  padding: 0 1rem;
  margin: 0 1rem;
  transition: all 0.2s ease;
}
#nav-link > a:hover{
  padding: 0 2rem;
}

#Navbar > button{
  border:none;
  padding: 0 0.5rem;
  color: white;
  background-color: rgb(217, 88, 80);
  text-align: center;
}
</style>
