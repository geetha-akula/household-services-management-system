import { createRouter, createWebHistory } from 'vue-router'
import store from '../store';

// Home
import HomeView from '../views/HomeView.vue'

// Authentication
import RegisterUser from '../auth/RegisterUser.vue'
import RegisterProfessional from '@/auth/RegisterProfessional.vue';
import LoginUser from '../auth/LoginUser.vue'
import LogoutUser from '@/auth/LogoutUser.vue';

// Admin Dashboard
import AdminDashboard from '../views/AdminDashboard.vue'
import AddService from '@/views/AddService.vue';
import EditService from '@/views/EditService.vue';
import ManageUsers from '@/views/ManageUsers.vue';
import ManageOrders from '@/views/ManageOrders.vue';
import AdminStats from '@/views/AdminStats.vue';


// User Dashboard
import UserDashboard from '../views/UserDashboard.vue'
import ServiceView from '@/views/ServiceView.vue';
import UserOrders from '@/views/UserOrders.vue';
import FeedbackForm from '@/views/FeedbackForm.vue';
import UserProfile from '../views/UserProfile.vue';


// Professional Dashboard
import ProfessionalDashboard from '../views/ProfessionalDashboard.vue';
import ProfessionalOrders from '@/views/ProfessionalOrders.vue';
import ProfessionalProfile from '../views/ProfessionalProfile.vue';



const routes = [
  
  {
    path: '/',
    name: 'home',
    component: HomeView
  },


  {
     path: '/login',
     name: 'login',
     component: LoginUser
  },
  {
    path: '/register-user',
    name:'register-user',
    component: RegisterUser
  },
  {
    path: '/register-professional',
    name:'register-professional',
    component: RegisterProfessional
  },
  {
    path: '/logout',
    name: 'logout',
    component: LogoutUser
  },


  
  {
    path: '/admin-dashboard',
    name: 'admin',
    component: AdminDashboard,
    meta: { requiresAuth:true, roles:['admin'] }
  },

  {
    path: '/addService',
    name: 'addService',
    component: AddService,
    meta: { requiresAuth:true, roles:['admin'] }
  },

  {
    path: '/editService',
    name: 'editService',
    component: EditService,
    meta: { requiresAuth:true, roles:['admin'] }
  },

  {
    path: '/manage-users',
    name: 'manage-users',
    component: ManageUsers,
    meta: { requiresAuth:true, roles:['admin'] }
  },

  {
    path: '/manage-orders',
    name: 'manage-orders',
    component: ManageOrders,
    meta: { requiresAuth:true, roles:['admin'] }
  },

  {
    path: '/admin-stats',
    name: 'admin-stats',
    component: AdminStats,
    meta: { requiresAuth:true, roles:['admin'] }
  },


  {
    path: '/user-dashboard',
    name: 'user',
    component: UserDashboard,
    meta: { requiresAuth: true, roles: ['user'] }
  },
  {
    path: '/service-view',
    name: 'service-view',
    component: ServiceView,
    meta: { requiresAuth: true, roles: ['user'] }
  },
  {
    path: '/user-orders',
    name: 'user-orders',
    component: UserOrders,
    meta: { requiresAuth: true, roles: ['user'] }
  },
  {
    path: '/feedback',
    name: 'feedback',
    component: FeedbackForm,
    meta: { requiresAuth: true, roles: ['user'] }
  },
  {
    path: '/user-profile',
    name: 'user-profile',
    component: UserProfile,
    meta: { requiresAuth: true, roles: ['user'] }
  },
 


  {
    path: '/professional-dashboard',
    name: 'professional',
    component: ProfessionalDashboard,
    meta: { requiresAuth: true, roles: ['professional'] }
  },

  {
    path: '/professional-orders',
    name: 'professional-orders',
    component: ProfessionalOrders,
    meta: { requiresAuth: true, roles: ['professional'] }
  },

  {
    path: '/professional-profile',
    name: 'professional-profile',
    component: ProfessionalProfile,
    meta: { requiresAuth: true, roles: ['professional'] }
  },

 

]


const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})



// Navigation Guarding
router.beforeEach((to, from, next) =>{
  if (to.meta.requiresAuth){
    if (!store.getters.isAuthenticated){
      next('/login')
    } else {
      console.log(store.getters.userRole);
      const userRole = store.getters.userRole;

      if (to.meta.roles && !to.meta.roles.includes(userRole)){
        next('/login');
      } else {
        next();
      }
    }
  } else {
    next();
  }
});

export default router
