<template>
    <div>
      <router-view/> 
    </div>
</template>


<script>

export default {
  name: 'App'
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

nav {
  padding: 10px 30px;
  text-align: end;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  width: 100%
}

.nav-title {
  font-size: 1.4rem;
  font-weight: bold;
  color: #b94289
}

nav a {
  margin-right: 20px;
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #b94289
}
</style>
