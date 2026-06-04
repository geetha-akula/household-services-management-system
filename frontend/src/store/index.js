import { createStore } from "vuex";
import router from "../router";
import { jwtDecode } from "jwt-decode";

export default createStore({
    state: {
        token: localStorage.getItem('token') || '',
        user: JSON.parse(localStorage.getItem('user') || null)
    },

    getters: {
        isAuthenticated: (state) => {
            if (state.token) {
                const decoded = jwtDecode(state.token);
                const currentTime = Math.floor(Date.now() / 1000);
                return decoded.exp > currentTime;

            }
            return false;
        },

        userRole: (state)=>{
            if (state.token){
                const decoded = jwtDecode(state.token);
                return decoded.sub;
            }
            return null;
        },
    },

    mutations: {
        setToken(state, token){
            state.token = token;
            if (token){
                localStorage.setItem('token', token);
            }
            else{
                localStorage.removeItem('token');
                localStorage.removeItem('user');
            }
        },
        setUser(state, user){
            state.user = user;
            if (user){
                localStorage.setItem('user', JSON.stringify(user));
            }
            else{
                localStorage.removeItem('user');
            }
        },
        logout(state){
            state.token = '';
            state.user = null;
            localStorage.removeItem('token');
            localStorage.removeItem('user');           
        }
    },

    actions: {
        login({commit},{token}){
            commit('setToken', token);

        },
        logout({commit}){
            commit('logout');
            router.push('/login');
        },
        checkTokenValidity({ commit, getters }) {
            if (!getters.isAuthenticated) {
                commit('logout');
                router.push('/login');
            }
        },
    },

});