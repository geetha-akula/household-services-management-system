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
    
        <div class="dashboard">
            <h3>Service Feedback Form</h3>

            <form @submit.prevent="submitFeedback" class="form-container">
                <div class="form-group">
                    <label for="serviceName">Service Name: </label>
                    <input type="text" id="serviceName" v-model="serviceName" readonly/>
                </div>

                <div class="form-group">
                    <label for="serviceDescription">Description: </label>
                    <textarea id="serviceDescription" v-model="serviceDescription" readonly></textarea>
                </div>

                <div class="form-group">
                    <label for="professionalName">Professional Name: </label>
                    <input id="professionalName" v-model="professionalName" readonly/>
                </div>

                <div class="form-group">
                    <label for="rating">Rating (1-5): </label>
                    <select class="rating" id="rating" v-model="rating">
                        <option disabled valued="">Select</option>
                        <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
                    </select>
                </div>

                <div class="button-group">
                <button type="submit" @click="submitFeedback(id)" class="submit">Submit</button>
                <button type="button" @click="cancelFeedback" class="cancel">Cancel</button>
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
            token: localStorage.getItem('token'),
            serviceName: '',
            serviceDescription: '',
            professionalName: '',
            rating: '',
            id: this.$route.query.id,

        }
    },

    created() {
        this.fetchServiceRequest(this.id);
    },

    methods: {
        async fetchServiceRequest(id) {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/api/service_request/${id}`,
                    {
                        headers: {
                            'Authorization': `Bearer ${this.token}`
                        },
                    },
                );

                this.request = response.data;

                this.serviceName = this.request.service_name;
                this.serviceDescription = this.request.service_description;
                this.professionalName = this.request.professional_name;


            } catch (error) {
                console.error('Error fetching service request', error);
            }
        },

        async submitFeedback(id){
            try {
                await axios.put('http://127.0.0.1:5000/api/user/feedback',
                    {
                        id: id,
                        rating: this.rating
                    },
                    {
                        headers: {
                            'Authorization': `Bearer ${this.token}`
                        },
                    },
              );
              alert('Feedback submitted successfully');
              this.$router.push('/user-orders');
            } catch (error) {
                console.error('Error submitting feedback', error);
            }
        },

        cancelFeedback(){
            this.$router.push('/user-orders');
            
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

.rating {
    width: 250px;
    height: 30px;
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

.submit {
    background-color: #4CAF50;
    color: white;
}

.cancel {
    background-color: #f44336;
    color: white;
}

</style>