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
    
        <div class="charts-container">
            <div class="chart-wrapper">
                <h3>User Count Graph</h3>
                <canvas ref="rolesChart"></canvas>
            </div>

            <div class="chart-wrapper">
                <h3>Count of Service Requests Status</h3>
                <canvas ref="statusChart"></canvas>
            </div>
                
            <div class="chart-wrapper">
                <h3>Count of Service Professionals</h3>
                    <canvas ref="professionalsChart"></canvas>
            </div> 
        </div>
    </div>
</template>
    
    
<script>
import axios from 'axios'
import { Chart } from 'chart.js';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, BarController, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, BarController, CategoryScale, LinearScale);


export default {
    data() {
        return {
            username: JSON.parse(localStorage.getItem('user')).username,
            token: localStorage.getItem('token'),

            roleschartData: {
                labels: [],
                datasets: [
                    {
                        label: 'Count of Users',
                        data: [],
                        backgroundColor: '#42A5F5'
                    },
                ],
            },
            
            statuschartData: {
                labels: [],
                datasets: [
                    {
                        label: 'Count of Service Requests',
                        data: [],
                        backgroundColor: '#FFA726',
                    }
                ],
            },

            professionalschartData: {
                labels: [],
                datasets: [
                    {
                        label: 'Count of Service Professionals',
                        data: [],
                        backgroundColor: '#66BB6A',
                    }
                ],
            },

            roleschartInstance: null,
            statuschartInstance: null,
            professionalschartInstance: null,
        };
    },

    mounted() {
        this.fetchStats();
    },

    methods: {
        async fetchStats(){
            try{
                const response = await axios.get('http://127.0.0.1:5000/api/stats',{
                    headers: {
                        'Authorization': `Bearer ${this.token}`
                    },
                });
                const data = response.data;

                // Update roles chart data
                this.roleschartData.labels = Object.keys(data.roles_count);
                this.roleschartData.datasets[0].data = Object.values(data.roles_count);

                // Update status chart data
                this.statuschartData.labels = Object.keys(data.status_count);
                this.statuschartData.datasets[0].data = Object.values(data.status_count);

                // Update professionals chart data
                this.professionalschartData.labels = Object.keys(data.professional_count);
                this.professionalschartData.datasets[0].data = Object.values(data.professional_count);

            
                // Call renderChart after upating chartData 
                this.renderRolesChart();
                this.renderStatusChart();
                this.renderProfessionalsChart();
            } catch(error) {
                console.error('Failed to fetch stats', error);
            }
        },

        renderRolesChart(){
            // Check if the canvas is available before trying to create the chart
            if (this.$refs.rolesChart){
                if (this.roleschartInstance) {
                    this.chartInstance.destroy();
                }

                this.roleschartInstance = new Chart(this.$refs.rolesChart.getContext('2d'), {
                    type: 'bar',
                    data: this.roleschartData,
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                display: true,
                                position: 'top',
                            },
                        },
                        scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: 'Categories',
                                },
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: 'Count',
                                },
                            }
                        },
                    }
                });
            } else {
                console.error('User Count Chart canvas not found');
            }
        },

        renderStatusChart(){
            // Check if the canvas is available before trying to create the chart
            if (this.$refs.statusChart){
                if (this.statuschartInstance) {
                    this.statuschartInstance.destroy();
                }

                this.statuschartInstance = new Chart(this.$refs.statusChart.getContext('2d'), {
                    type: 'bar',
                    data: this.statuschartData,
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                display: true,
                                position: 'top',
                            },
                        },
                        scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: 'Status',
                                },
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: 'Count',
                                },
                            }
                        },
                    }
                });
            } else {
                console.error('Service Requests Status Chart canvas not found');
            }
        },

        renderProfessionalsChart(){
            // Check if the canvas is available before trying to create the chart
            if (this.$refs.professionalsChart){
                if (this.professionalschartInstance) {
                    this.professionalschartInstance.destroy();
                }

                this.professionalschartInstance = new Chart(this.$refs.professionalsChart.getContext('2d'), {
                    type: 'bar',
                    data: this.professionalschartData,
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                display: true,
                                position: 'top',
                            },
                        },
                        scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: 'Services',
                                },
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: 'Count of Professionals',
                                },
                            }
                        },
                    }
                });
            } else {
                console.error('Professionals Chart canvas not found');
            }

        },
        
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

.dashboard {
    padding: 20px;
}


.charts-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    padding: 10px;
    background-color: #f4f4f4;
}

.chart-wrapper {
    width: 550px;
    padding: 20px;
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h3 {
    margin-bottom: 20px;
    text-align: center;
}


</style>