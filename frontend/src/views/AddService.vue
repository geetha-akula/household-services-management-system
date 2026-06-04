<template>
    <div>
        <nav>
            <div class="nav-container">
              <div class="nav-title">
                Admin Dashboard
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
            <h3>Add New Service</h3>

            <form @submit.prevent="addService" class="form-container">
                <div class="form-group">
                    <label for="serviceName">Service Name: </label>
                    <input type="text" id="serviceName" v-model="newServiceName" placeholder="Enter service name" required>
                </div>

                <div class="form-group">
                    <label for="serviceDescription">Description: </label>
                    <textarea id="serviceDescription" v-model="newServiceDescription" placeholder="Enter service description"></textarea>
                </div>

                <div class="form-group">
                    <label for="servicePrice">Price: </label>
                    <input type="number" id="servicePrice" v-model="newServicePrice" placeholder="Enter service price" required min="0">
                </div>

                <div class="form-group">
                    <label for="serviceTimeRequired">Time Required (in hrs): </label>
                    <input type="number" id="serviceTimeRequired" v-model="newServiceTimeRequired" placeholder="Enter service time required" min="0" step="0.1">
                </div>

                <div class="button-group">
                <button type="submit" @click="addService" class="add">Add Service</button>
                <button type="button" @click="cancelService" class="cancel">Cancel</button>
                </div>

            </form>
        </div>
            
    </div>
    </template>
    
    
    <script>
    import axios from 'axios'
    
    export default {
        data() {
            return {
                username: JSON.parse(localStorage.getItem('user')).username,
                newServiceName: '',
                newServiceDescription: '',
                newServicePrice: null,
                newServiceTimeRequired: null,
            }
        },
    
        methods: {
            async addService(){
            try {
                const token = localStorage.getItem('token');
                const response = await axios.post('http://127.0.0.1:5000/api/service',{
                    name: this.newServiceName,
                    description: this.newServiceDescription,
                    price: this.newServicePrice,
                    time_required: this.newServiceTimeRequired
                }, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                });
                console.log('Service added', response.data);
                this.newServiceName = '';
                this.newServiceDescription = '';
                this.newServicePrice = null;
                this.newServiceTimeRequired = null;
                this.$router.push('/admin-dashboard');
                
            } catch (error) {
                console.error('Error adding service', error);
            }
        },

        cancelService(){
            this.newServiceName = '';
            this.newServiceDescription = '';
            this.newServicePrice = null;
            this.newServiceTimeRequired = null;
            this.$router.push('/admin-dashboard');
                
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

h3 {
    margin-bottom: 20px;
    text-align: center;
    font-size: 24px;
}

.form-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 500px;
    margin: 0 auto;

}

.form-group {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-bottom: 15px;

}

label {
    flex: 1;
    text-align: left;
    margin-right: 10px;
    font-weight: bold;
}

input, textarea {
    flex: 1;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
}

textarea {
    height: 100px;
}

.button-group {
    display:flex;
    justify-content: space-between;
    width:100%;
    margin-top: 10px;
}

button {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

.add {
    background-color: #4CAF50;
    color: white;
}

.cancel {
    background-color: #f44336;
    color: white;
}

</style>