<template>
  <div>
    <nav>
        <div class="nav-container">
          <div class="nav-title">
            Maruthi Household Services
          </div>

          <div class="nav-links">  
            <router-link to="/">Home</router-link>
            <router-link to="/login">Login</router-link>
          </div>
        </div>
    </nav>

    <div class="home">
        <br/><br/><br/><br/><br/><br/>
        <h1>Welcome to our Online Household Services app</h1>
        <p>This app will help you manage your household tasks, budget, and expenses efficiently.</p>
        <router-link to="/login">Get Started</router-link>
    </div>

  </div>
</template>

<script>

</script>

<style scoped>

.home a {
  margin-right: 20px;
  font-weight: bold;
  color: #b94289;
}

</style>