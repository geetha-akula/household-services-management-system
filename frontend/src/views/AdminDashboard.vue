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
            <div v-if="filteredServices.length>0">
                <h2> Available Services </h2>
                <div class="services">
                    <div v-for="service in filteredServices" 
                        :key="service.id"
                        class = "service-card">
                        <h3>{{ service.name }}</h3>
                        <p>{{ service.description }}</p>
                        <p>Price: ₹{{ service.price }}</p>
                        <p v-if="service.time_required">Duration: {{ service.time_required }} hr</p>
                        <button class="edit-button" @click="editService(service.id)">Edit</button>
                        <button class="delete-button" @click="deleteService(service.id)">Delete</button>
                    </div>
                </div>
                <button class="new-service-btn" @click="addNewService">+ New Service</button>
            </div>
            <div v-else>
                <h2>No services available</h2>
            </div>
        </div>
            
    </div>
    </template>
    
    
    <script>
    import axios from 'axios'
    
    export default {
        data() {
            return {
                token: localStorage.getItem('token'),
                username: JSON.parse(localStorage.getItem('user')).username,
                services: [],
                filteredServices: [],
                searchQuery: ''
            }
        },
    
        mounted() {
            this.fetchServices();
        },
    
        methods: {
            async fetchServices() {
                try {
                    const response = await axios.get('http://127.0.0.1:5000/api/service', {
                        headers: 
                        { 
                            
                            Authorization: `Bearer ${this.token}` 

                        }
                    });
                    this.services = response.data;
                    this.filteredServices = this.services;
                    
                } catch (error) {
                    console.error('Error loading services', error);
                }
            },
    
            handleSearch() {
                const query = this.searchQuery.toLowerCase();
                this.filteredServices = this.services.filter(service =>
                    service.name.toLowerCase().includes(query)
                );
            },

            addNewService() {
                this.$router.push('/addService');
            },

            editService(id){
                this.$router.push({ name: "editService", query: {id: id}});
            },

            async deleteService(id){
                if (!confirm('Are you sure you want to delete this service?')) 
                    return;

                try {
                const response = await axios.delete('http://127.0.0.1:5000/api/service',{
                    data: { id: id },
                });
                alert(response.data.message);
                console.log(response.data);
                this.fetchServices();
                
            } catch (error) {
                console.error('Error deleting service', error);
                alert("Failed to delete the service.");
            }

        },
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
    
    .services {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
    }
    
    .service-card{
        border: 1px solid black;
        padding: 15px;
        border-radius: 5px;
        cursor: pointer;
        transition: box-shadow 0.3s;
        width: 200px;
        height: 200px;
    }
    
    .service-card:hover {
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }

    .edit-button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
        cursor: pointer;
        margin-right: 5px;
    }

    .delete-button {
        background-color: #f44336;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
        cursor: pointer;
    }

    .new-service-btn {
        background-color: #4caf50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 50px;
        cursor: pointer;
        position: absolute;
        bottom: 20px;
        right: 20px;
        font-size: 16px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
    }

    .new-service-btn:hover {
        background-color: #0b990b;
    }
    
    </style>