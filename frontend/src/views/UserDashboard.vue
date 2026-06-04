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
        <div v-if="filteredServices.length>0">
            <h2> Available Services </h2>
            <div class="services">
                <div v-for="service in filteredServices" 
                    :key="service.id"
                    class = "service-card"
                    @click = "openService(service.id)">

                    <h3>{{ service.name }}</h3>
                    <p>{{ service.description }}</p>
                    <p>Price: ₹{{ service.price }}</p>
                    <p v-if="service.time_required">Duration: {{ service.time_required }}hr</p>
                </div>
            </div>
        </div>
        <div v-else>
            <h2>No services available</h2>
            <p>Please check back later for available services.</p>
        </div>
    </div>
        
</div>
</template>


<script>
import axios from 'axios'

export default {
    data() {
        return {
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
                const response = await axios.get('http://127.0.0.1:5000/api/service', 
                );
                this.services = response.data;
                this.filteredServices = this.services;
                
            } catch (error) {
                console.error('Error loading services', error);
            }
        },

        openService(serviceID){
            this.$router.push({ name: 'service-view', query: { serviceID } });
        },

        handleSearch() {
            const query = this.searchQuery.toLowerCase();
            this.filteredServices = this.services.filter(service =>
                service.name.toLowerCase().includes(query)
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

</style>
