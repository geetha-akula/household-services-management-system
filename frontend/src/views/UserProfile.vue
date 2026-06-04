<template>
    <div>
        <nav>
            <div class="nav-container">
              <div class="nav-title">
                Customer Dashboard
              </div>
    
              <div class="nav-links">  
                <router-link to="/user-dashboard">Home</router-link>
                <router-link to="/user-orders">Orders</router-link>
                <router-link to="/user-profile">Profile</router-link>
                <router-link to="/logout">Logout</router-link>
                <span>{{ username }}</span>
              </div>
            </div>
        </nav>

        <div class="user-profile">
            <h2> User Profile</h2>
                
            <div class="profile-details">
                <div class="detail"><strong>Username: </strong>
                    <span>{{ user.username }}</span>
                </div>
                <div class="detail"><strong>Email: </strong>
                    <span>{{ user.email }}</span>
                </div>
                <div class="detail"><strong>Location: </strong>
                    <span>{{ user.location || 'NA' }}</span>
                </div>
                <div class="detail"><strong>Pincode: </strong>
                    <span>{{ user.pincode || 'NA' }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            username: JSON.parse(localStorage.getItem('user')).username,
            user: {},
            email: '',
            location: '',
            pincode: ''
        };
    },

    async created() {
        this.fetchUserDetails();
    },

    methods: {
        async fetchUserDetails() {
            try {
                const id = JSON.parse(localStorage.getItem('user')).id;
                const response = await axios.get(`http://127.0.0.1:5000/api/user/${id}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    },
                });
                this.user = response.data;
            } catch (error) {
                console.error("Error fetching user profile", error);
            }
        },
    }
}

</script>



<style scoped>

/* span {
    color: #b94289;
    font-weight: bold;
} */

.profile-details {
    margin: 20px 0;
    padding: 50px;
}

.detail {
    margin-bottom: 20px;
    display:block;
}


</style>