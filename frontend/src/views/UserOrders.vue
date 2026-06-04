<template>
    <div>
        <nav>
            <div class="nav-container">
              <div class="nav-title">
                Customer Dashboard
              </div>
    
              <div class="nav-search">
                  <input type="text" placeholder="Search" v-model="searchQuery"
                   @input="handleSearch"> 
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

        <div class="dashboard">
            <h2>Service History</h2>

            <table v-if="filteredOrders.length >0">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Service Name</th>
                        <th>Professional Name</th>
                        <th>Location</th>
                        <th>Requested Date</th>
                        <th>Completion Date</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="(order,index) in filteredOrders" :key="order.id">
                        <td>{{ index+1 }}</td>
                        <td>{{ order.service_name }}</td>
                        <td>{{ order.professional_name }}</td>
                        <td>{{ order.location }}</td>
                        <td>{{ order.requested_date }}</td>
                        <td>{{ order.completion_date }}</td>
                        <td>{{ order.service_status }}</td>
                        <td>
                            <button class="cancel" v-if="order.service_status === 'requested'" 
                                    @click="cancelOrder(order.id)">Cancel</button>
                            <button class="close" v-if="order.service_status === 'assigned'"
                                    @click="updateOrderStatus(order.id)">Close</button>
                            <button class="feedback" v-if="order.service_status === 'closed' && !order.rating"
                                    @click="feedback(order.id)">Feedback</button>
                        </td>
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
            searchQuery: ""
        };
    },

    mounted() {

        this.fetchOrders(this.id);
    },

    methods: {
        async fetchOrders(id) {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/api/user/${id}/orders`, {
                    headers: {
                        'Authorization': `Bearer ${this.token}`,
                    },
                });
                this.orders = response.data;
                this.filteredOrders = this.orders;

            } catch (error) {
                console.error("Error fetching orders", error);
            }
        },

        async cancelOrder(id){
            try {
                await axios.delete(`http://127.0.0.1:5000/api/service_request/${id}/cancel`,
                {
                        headers: {
                            'Authorization': `Bearer ${this.token}`,
                        },
                    }
                );
                this.fetchOrders(this.id);
            } catch(error) {
                console.error("Error canceling order", error);
            }
        },

        async updateOrderStatus(id){
            try {
                await axios.put(`http://127.0.0.1:5000/api/service_request/${id}/close`, {}, {
                        headers: {
                            'Authorization': `Bearer ${this.token}`,
                        },
                    }
                );
                this.fetchOrders(this.id);
            } catch(error) {
                console.error("Error updating order status", error);
            }
            this.fetchOrders(this.id);
        },

        async feedback(id){
            this.$router.push({ name: "feedback", query: {id: id}})
        },

        handleSearch() {
            const query = this.searchQuery.toLowerCase();
            this.filteredOrders = this.orders.filter(order => 
                order.service_name.toLowerCase().includes(query) ||
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

button.cancel {
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease;
}

button.cancel:hover {
    background-color: #d32f2f;
}


button.close {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease;
}

button.close:hover {
    background-color: #0a73e3;
}


button.feedback {
    background-color: #04e3ef;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease;
}

button.feedback:hover {
    background-color: #09d6e0;
}



span {
    color: #b94289;
    font-weight: bold;
}

</style>
