import {defineStore} from 'pinia'
import axios from 'axios';
import router from '@/router';

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => {
        return {
            accessToken: null,
            refreshToken: null,
            username: null,
            email: null,
        }
    },
    getters:{
        getAccessToken(state): string | null{
            return state.accessToken;
        },
        getRefresshToken(state): string | null{
            return state.refreshToken;
        }
    },
    actions:{
        loadTokenFromLocalStorage(tokenKey: string){
            const accessToken = localStorage.getItem(tokenKey);
            if (accessToken)
                this[tokenKey] = accessToken
        },
        tryRefreshToken(){
            const refreshToken = this.refreshToken
            return axios.post('/api/refreshtoken', {refresh_token: refreshToken})
        },
        tryAuthenticate(){
            const accessToken = this.accessToken? this.accessToken : ""
            return axios.post('http://localhost/oauth/authorize', {access_token: accessToken, token_type: 'bearer'})
        },
        setUsername(username: string){
            this.username = username
        },
        setEmail(email: string){
            this.email = email
        },
        logout(){
            localStorage.removeItem("accessToken");
            router.go()
        }

    }
})
