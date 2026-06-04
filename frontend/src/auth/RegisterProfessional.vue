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
        <form @submit.prevent = "RegisterProfessional">
            <h2>Professional Signup</h2>
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
                <label for="service_type"><b>Service Type: </b> </label>
                <select id="service_type" v-model="service_type" required>
                    <option value="" disabled> Select a service </option>
                    <option v-for="service in services" :key="service.id" :value="service.name">
                        {{ service.name }}
                    </option>
                </select>
            </div>
            <br/>
            <div class="form-group">
                <label for="experience"><b>Experience: </b> </label>
                <input type="number" id="experience" min="0" v-model="experience" required>
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
            <button type="submit">Register</button>

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
            experience: '',
            service_type: '',
            services: [],
            role: 'user',
            errorMessage: ''
        };
    },

    mounted(){
            this.fetchServices();
    },


    methods: {       
        async fetchServices(){
            try{
                const response = await axios.get('http://127.0.0.1:5000/api/service');
                this.services = response.data;

            } catch(error) {
                console.error('Error fetching services', error);
            }
        },

        async RegisterProfessional(){
            try{
                await axios.post('/api/register',{
                    username: this.username,
                    email: this.email,
                    password: this.password,
                    location: this.location,
                    pincode: this.pincode,
                    experience: this.experience,
                    service_type: this.service_type,
                    role: 'professional'
                });
                this.$router.push('/login');

            } catch(error){
                this.errorMessage = error.response ? error.response.data.message:
                'An error occurred while registering the professional.';
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
    height: 80vh;
}

.login-container a {
    color: #b94289;
}

input {
    width: 250px;
    padding: 4px;
}

select {
    width: 250px;
    padding: 6px;
}

</style>