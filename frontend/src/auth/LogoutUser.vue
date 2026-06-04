<template>
  <div>
  </div>
</template>

<script>

export default {
   mounted() {
     this.logoutUser();
   },

   methods: {
     logoutUser() {
       localStorage.removeItem('token');
       localStorage.removeItem('user')
       this.$router.push('/');
     }
   }
 };

</script>

<style scoped>

</style>
