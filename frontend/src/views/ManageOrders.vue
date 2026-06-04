<template>
    <div>
        <nav>
            <div class="nav-container">
              <div class="nav-title">
                Admin Dashboard
              </div>
    
              <div class="nav-search">
                  <input type="text" placeholder="Search" v-model="searchQuery"
                   @input="handleSearch">  
              </div>
    
              <div class="nav-links">  
                <router-link to="/admin-dashboard">Home</router-link>
                <router-link to="/manage-users">Users</router-link>
                <router-link to="/manage-orders">Orders</router-link>
                <router-link to="/admin-stats">Stats</router-link>
                <router-link to="/logout">Logout</router-link>
                <span>{{ username }}</span>
              </div>
            </div>
        </nav>
    
        <div class="dashboard">
            <h2>Service Requests</h2>

            <table v-if="filteredRequests.length >0">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Service Name</th>
                        <th>Assigned Professional</th>
                        <th>Customer Name</th>
                        <th>Requested Date</th>
                        <th>Completion Date</th>
                        <th>Rating</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(request, index) in filteredRequests" :key="request.id">
                        <td>{{ index+1 }}</td>
                        <td>{{ request.service_name }}</td>
                        <td>{{ request.professional_name }}</td>
                        <td>{{ request.customer_name }}</td>
                        <td>{{ request.requested_date }}</td>
                        <td>{{ request.completion_date }}</td>
                        <td>{{ request.rating }}</td>
                        <td>{{ request.service_status }}</td>
                    </tr>
                </tbody>

            </table>
            <div v-else>
                <p>No service requests found.</p>
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
            serviceRequests: [],
            filteredRequests: [],
            searchQuery: ''
        }
    },

    mounted() {
        this.fetchServiceRequests();
    },

    methods: {
        async fetchServiceRequests() {
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get('http://127.0.0.1:5000/api/service_requests', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });
                this.serviceRequests = response.data;
                this.filteredRequests = this.serviceRequests;
                
            } catch (error) {
                console.error('Error fetching service requests', error);
            }
        },


        handleSearch() {
            const query = this.searchQuery.toLowerCase();
            this.filteredRequests = this.serviceRequests.filter(request =>
                request.service_name.toLowerCase().includes(query) ||
                request.professional_name.toLowerCase().includes(query) ||
                request.customer_name.toLowerCase().includes(query) ||
                request.requested_date.toLowerCase().includes(query) ||
                request.service_status.toLowerCase().includes(query)
            );
        }
    }
}

</script>



<style scoped>

.nav-search input {
    width: 200px;
    border: 1px solid black;
    border-radius: 4px;

}

span {
    color: #b94289;
    font-weight: bold;
}

.dashboard {
    padding: 20px;
}


table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    font-size: 16px;
    text-align: center;
}

table th{
    background-color: #f4f4f4;
    color: #333;
    padding: 10px;
    border: 1px solid #ddd;
}

table tbody tr {
    transition: background-color 0.3s ease;
}

table tbody tr:hover {
    background-color: #f9f9f9;
}

table tbody td {
    padding: 10px;
    border: 1px solid #ddd;
}

</style>