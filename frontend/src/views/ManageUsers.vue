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
            <h2>Pending Professionals</h2>
            <table v-if=" pendingProfessionals && pendingProfessionals.length>0">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Location</th>
                        <th>Pincode</th>
                        <th>Service Type</th>
                        <th>Experience (in years)</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(professional,index) in pendingProfessionals" :key="professional.id">
                        <td> {{ index+1 }}</td>
                        <td> {{  professional.username }} </td>
                        <td> {{  professional.email }} </td>
                        <td> {{  professional.location }} </td>
                        <td> {{  professional.pincode }} </td>
                        <td> {{  professional.service_type }} </td>
                        <td> {{  professional.experience }} </td>
                        <td>
                            <button class="approve" @click="approveProfessional(professional.id)">Approve</button>
                            <button class="reject" @click="rejectProfessional(professional.id)">Reject</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <p v-else>No pending professionals available</p>


            <h2>Users</h2>
            <table v-if="filteredusers.length>0">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Location</th>
                        <th>Pincode</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(user, index) in filteredusers" :key="user.id">
                        <td> {{ index+1 }}</td>
                        <td> {{  user.username }} </td>
                        <td> {{  user.email }} </td>
                        <td> {{  user.location }} </td>
                        <td> {{  user.pincode }} </td>
                    </tr>
                </tbody>
            </table>
            <p v-else>No users available</p>


            <h2>Professionals</h2>
            <table v-if="filteredprofessionals.length>0">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Location</th>
                        <th>Pincode</th>
                        <th>Service Type</th>
                        <th>Experience(in years)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(professional, index) in filteredprofessionals" :key="professional.id">
                        <td> {{ index+1 }} </td>
                        <td> {{  professional.username }} </td>
                        <td> {{  professional.email }} </td>
                        <td> {{  professional.location }} </td>
                        <td> {{  professional.pincode }} </td>
                        <td> {{  professional.service_type }} </td>
                        <td> {{  professional.experience }} </td>
                    </tr>
                </tbody>
            </table>
            <p v-else>No professionals available</p>

        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default{
    data(){
        return {
            username: JSON.parse(localStorage.getItem('user')).username,
            token: localStorage.getItem('token'),
            id: JSON.parse(localStorage.getItem('user')).id,
            pendingProfessionals: [],
            users: [],
            professionals: [],
            filteredusers: [],
            filteredprofessionals: [],
            searchQuery: '',
        }
    },

    created(){
        this.fetchPendingProfessionals();
        this.fetchUsers();
        this.fetchProfessionals();
    },

    methods: {
        async fetchPendingProfessionals(){
            await axios.get('http://127.0.0.1:5000/api/pending_professionals', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                },
            })
            .then((response)=>{
                this.pendingProfessionals = response.data;
            })
            .catch((error)=>{
                console.error(error);
            })
        },
    
        async approveProfessional(id){
            const data = {
                professional_id: id,
                status: 'approve',
            };

            if (!confirm('Are you sure you want to approve this professional?')) 
                return;
            
            await axios.post('http://127.0.0.1:5000/api/pending_professionals', data,{
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                },
            })
            .then((response)=>{
                alert(response.data.message);
                this.fetchPendingProfessionals();
                this.fetchProfessionals();
                console.log(response.data);
            })
            .catch((error)=>{
                console.error(error);
            })
        },


        
        async rejectProfessional(id){
            const data = {
                professional_id: id,
                status: 'reject',
            };

            if (!confirm('Are you sure you want to reject this professional?')) 
                return;
            
            await axios.post('http://127.0.0.1:5000/api/pending_professionals', data,{
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                },
            })
            .then((response)=>{
                alert(response.data.message);
                this.fetchPendingProfessionals();
                console.log(response.data);
            })
            .catch((error)=>{
                console.error(error);
            })
        },
        
        async fetchUsers(){
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/users', {
                    headers: {
                        'Authorization': `Bearer ${this.token}`
                    },
                });
                this.users = response.data;
                this.filteredusers = this.users;
                console.log(this.users);

            } catch (error) {
                console.error(error);
            }
        },

        async fetchProfessionals(){
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/professionals', {
                    headers: {
                        'Authorization': `Bearer ${this.token}`
                    },
                });
                this.professionals = response.data;
                this.filteredprofessionals = this.professionals;
                console.log(this.professionals);
            } catch (error) {
                console.error(error);
            }
        },

        handleSearch() {
            const query = this.searchQuery.toLowerCase();

            this.filteredusers = this.users.filter(user => 
                user.username.toLowerCase().includes(query) ||
                user.location.toLowerCase().includes(query)
            );

            this.filteredprofessionals = this.professionals.filter(professional => 
                professional.username.toLowerCase().includes(query) ||
                professional.location.toLowerCase().includes(query) ||
                professional.service_type.toLowerCase().includes(query) ||
                professional.experience.toString().includes(query)
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
    margin-top: 30px;
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

button.approve {
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

button.approve:hover {
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

</style>