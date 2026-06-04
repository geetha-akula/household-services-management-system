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
            <h2> Professionals Offering {{ serviceName }} Service</h2>
            <table v-if="filteredprofessionals.length>0">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Experience (in years)</th>
                        <th>Location</th>
                        <th>Pincode</th>
                        <th>Action</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="(professional,index) in filteredprofessionals" :key="professional.id">
                        <td>{{ index+1 }}</td>
                        <td>{{ professional.username }}</td>
                        <td>{{ professional.experience }}</td>
                        <td>{{ professional.location }}</td>
                        <td>{{ professional.pincode }}</td>
                        <td>
                            <button @click="handleBookProfessional(professional)">Book</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div v-else>
                <p>Currently no professionals available</p>
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
            username: JSON.parse(localStorage.getItem('user')).username,
            token: localStorage.getItem('token') || "",
            professionals: [],
            filteredprofessionals: [],
            serviceName: "",
            searchQuery: ''
        }
    },
    mounted() {
        const serviceID = this.$route.query.serviceID;
        this.fetchProfessionals(serviceID);
    },

    methods: {
        async fetchProfessionals(serviceID) {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/api/service/${serviceID}/professionals`, {
                    headers: {
                        'Authorization': `Bearer ${this.token}`
                    },
                });

                const {service_name, professionals} = response.data;

                this.serviceName = service_name;
                this.professionals = professionals;
                this.filteredprofessionals = this.professionals;

            } catch(error) {
                console.error( "Error fetching professionals", error);
            }
        },

        async handleBookProfessional(professional) {
            try {
                    await axios.post('http://127.0.0.1:5000/api/service_request/create',{
                    service_id: this.$route.query.serviceID,
                    customer_id: JSON.parse(localStorage.getItem('user')).id,
                    professional_id: professional.id
                },
                {
                    headers: {
                        'Authorization': `Bearer ${this.token}`,
                    },
                });
                alert("Service booked successfully!");
            } catch(error) {
                console.error("Error booking service", error);
            }
        },

        handleSearch() {
            const query = this.searchQuery.toLowerCase();
            this.filteredprofessionals = this.professionals.filter(professional => 
                professional.location.toLowerCase().includes(query) ||
                professional.pincode.includes(query)  ||
                professional.experience.toString().includes(query)
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

button {
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #0b990b;
}


span {
    color: #b94289;
    font-weight: bold;
}

</style>