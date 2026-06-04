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
            <h2>Service History</h2>
            <table v-if="filteredOrders.length > 0">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Customer Name</th>
                        <th>Loaction</th>
                        <th>Requested Date</th>
                        <th>Completion Date</th>
                        <th>Status</th>
                        <th>Rating</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(order,index) in filteredOrders" :key="order.id">
                        <td>{{ index+1. }}</td>
                        <td>{{ order.customer_name }}</td>
                        <td>{{ order.location }}</td>
                        <td>{{ order.requested_date }}</td>
                        <td>{{ order.completion_date }}</td>
                        <td>{{ order.service_status }}</td>
                        <td>{{ order.rating }}</td>
                    </tr>
                </tbody>

            </table>
            <div v-else>
                <p>No service history found.</p>
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
            id: JSON.parse(localStorage.getItem('user')).id,
            token: localStorage.getItem('token'),
            orders: [],
            filteredOrders: [],
            searchQuery: '',
        }
    },
    mounted() {
        this.fetchOrders(this.id);
    },

    methods: {
        async fetchOrders(id) {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/api/professional/${id}/orders`, {
                    headers: {
                        'Authorization': `Bearer ${this.token}`,
                    },
                });
                this.orders = response.data;
                console.log(this.orders);
                this.filteredOrders = this.orders;

            } catch (error) {
                console.error("Error fetching orders", error);
            }
        },

        handleSearch() {
            const query = this.searchQuery.toLowerCase();
            this.filteredOrders = this.orders.filter(order => 
                order.location.toLowerCase().includes(query) ||
                order.requested_date.toString().includes(query) ||
                order.service_status.toLowerCase().includes(query)
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

span {
    color: #b94289;
    font-weight: bold;
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


</style>