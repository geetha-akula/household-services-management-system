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
    <div class="register-container">
        <form @submit.prevent = "RegisterUser">
            <h2>Customer Signup</h2>
            <br/>
            <div class="form-group">
                <label for="username"><b>Username: </b></label>
                <input type="text"  id="username" v-model="username" required>
            </div>
            <br/>
            <div class="form-group">
                <label for="email"><b>Email ID : </b> </label>
                <input type="email"  id="email" v-model="email" required>
            </div>
            <br/>
            <div class="form-group">
                <label for="password"><b>Password: </b> </label>
                <input type="password" id="password" v-model="password" required>
            </div>
            <br/>
            <div class="form-group">
                <label for="location"><b>Location: </b> </label>
                <input type="text" id="location" v-model="location" required>
            </div>
            <br/>
            <div class="form-group">
                <label for="pincode"><b>PinCode: </b> </label>
                <input type="text" id="pincode" v-model="pincode" required>
            </div>
            <br/>
            <button type="submit"> Register </button>

        </form>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
</div>

</template>

<script>
import axios from 'axios';

export default{
    data() {
        return {
            username: '',
            email: '',
            password: '',
            location: '',
            pincode: '',
            role: 'user',
            errorMessage: ''
        };
    },
    methods: {
        async RegisterUser(){
            try{
                await axios.post('/api/register',{
                    username: this.username,
                    email: this.email,
                    password: this.password,
                    location: this.location,
                    pincode: this.pincode,
                    role: 'user'
                });
                this.$router.push('/login');
            } catch(error){
                this.errorMessage = error.response ? error.response.data.message:
                'An error occurred while registering the user.';
            }
        }
    }
}
</script>

<style scoped>

.register-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 70vh;
}

.login-container a {
    color: #b94289;
}

input {
    width: 250px;
    padding: 4px;
}

</style>