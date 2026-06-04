<template>
    <div>
        <nav>
            <div class="nav-container">
              <div class="nav-title">
                Professional Dashboard
              </div>
    
              <div class="nav-search">
                  <input type="text" placeholder="Search" v-model="searchQuery"
                   @input="handleSearch">  
              </div>
    
              <div class="nav-links">  
                <router-link to="/professional-dashboard">Home</router-link>
                <router-link to="/professional-orders">Orders</router-link>
                <router-link to="/professional-profile">Profile</router-link>
                <router-link to="/logout">Logout</router-link>
                <span>{{ username }}</span>
              </div>
            </div>
        </nav>

        <div class="dashboard">
            <h2> Service Requests </h2>
            <table v-if="filteredRequests.length>0">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Customer Name</th>
                        <th>Location</th>
                        <th>Pincode</th>
                        <th>Requested Date</th>
                        <th>Action</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="(request,index) in filteredRequests" :key="request.id">
                        <td>{{ index+1 }}</td>
                        <td>{{ request.customer_name }}</td>
                        <td>{{ request.location }}</td>
                        <td>{{ request.pincode }}</td>
                        <td>{{ request.requested_date }}</td>
                        <td>
                            <button class="accept" @click="handleAccept(request.id)">Accept</button>
                            <button class="reject" @click="handleReject(request.id)">Reject</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div v-else>
                <p>Currently no requests available</p>
                <p>Please check later</p>
            </div>

        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            id : JSON.parse(localStorage.getItem('user')).id,
            username: JSON.parse(localStorage.getItem('user')).username,
            token: localStorage.getItem('token') || "",
            serviceRequests: [],
            filteredRequests: [],
            searchQuery: ''
        }
    },
    mounted() {
        this.fetchServiceRequests(this.id);
    },

    methods: {
        async fetchServiceRequests(id) {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/api/professional/${id}/requests`, {
                    headers: {
                        'Authorization': `Bearer ${this.token}`
                    },
                });

                this.serviceRequests = response.data;
                this.filteredRequests = this.serviceRequests;

            } catch(error) {
                console.error( "Error fetching requests", error);
            }
        },

        async handleAccept(id) {
            try {
                    await axios.post(`http://127.0.0.1:5000/api/service_request/${id}/accept`, {}, {
                    headers: {
                        'Authorization': `Bearer ${this.token}`,
                    },
                });

                alert("Request accepted!");
                this.fetchServiceRequests();

            } catch(error) {
                console.error("Error accepting request", error);
            }
            this.fetchServiceRequests(this.id);
        },

        async handleReject(id) {
            try {
                    await axios.delete(`http://127.0.0.1:5000/api/service_request/${id}/reject`, {
                    headers: {
                        'Authorization': `Bearer ${this.token}`,
                    },
                });

                alert("Request rejected!");
                this.fetchServiceRequests(this.id);

            } catch(error) {
                console.error("Error rejecting request", error);
            }
            this.fetchServiceRequests(this.id);
        },

        handleSearch() {
            const query = this.searchQuery.toLowerCase();
            this.filteredRequests = this.serviceRequests.filter(request => 
                request.location.toLowerCase().includes(query) ||
                request.pincode.includes(query)  ||
                request.requested_date.toString().includes(query)
            );
        }
        
    },
};


</script>



<style scoped>

.nav-search input {
   width: 200px;
   border: 1px solid black;
   border-radius: 4px;

}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px 0;
    font-size: 16px;
    text-align: center;
}

table thead th{
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

button.accept {
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease;
    margin-right: 10px;
}

button.accept:hover {
    background-color: #45a049;
}


button.reject {
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease;
}

button.reject:hover {
    background-color: #d32f2f;
}



span {
    color: #b94289;
    font-weight: bold;
}

</style>