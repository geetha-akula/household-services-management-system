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
   <div class="login-container">
        <form @submit.prevent = "LoginUser">
            <h2>Login Page</h2>
            <br/><br/>
            <div class="form-group">
                <label for="username"><b>Username: </b></label>
                <input type="text"  id="username" v-model="username" required>
            </div>
            <br/>
            <div class="form-group">
                <label for="password"><b>Password: </b></label>
                <input type="password" id="password" v-model="password" required>
            </div>
            <br/>
            <div>
                <button type="submit">Login</button>
            </div>
                <p>New user? &VeryThinSpace;Register as
                    <br/>
                    <RouterLink to="/register-user">user</RouterLink> &VeryThinSpace;
                    <RouterLink to="/register-professional">professional</RouterLink>
                </p>

        </form>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
</div>
</template>

<script>
    import axios from 'axios';
    export default {
        data() {
            return {
                username: '',
                password: '',
                errorMessage: ''
            }
        },
        methods: {
            async LoginUser() {
                try {
                    const response = await axios.post('http://127.0.0.1:5000/api/login', {
                        username: this.username,
                        password: this.password
                    });

                    console.log(response);
                    const {access_token, user} = response.data;
                    localStorage.setItem('user', JSON.stringify(user));
                    this.$store.dispatch('login', {token: access_token,user});

                    console.log(user.role);
                 
                    if ( user.role === 'admin' ){
                        this.$router.push('/admin-dashboard')
                    }   
                    else if ( user.role === 'professional'){
                        this.$router.push('/professional-dashboard')
                    }
                    else {
                        this.$router.push('/user-dashboard')
                    }
                }
                catch (error) {
                    console.log(error);
                    this.errorMessage = error.response ? error.response.data.message:
                    'Invalid credentials';
                }
            }
        }
    }
</script>

<style scoped>

.login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 60vh;
}

.login-container a {
    color: #b94289;
}

input {
    width: 250px;
    padding: 4px;
}

</style>