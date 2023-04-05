import axios from 'axios';
import jwtDecode from 'jwt-decode';
import {useAuthStore} from '@/stores/auth';

const API_URL = 'http://localhost';

type LoginData = {
    identifier: string,
    password: string
}
class AuthService {
    login(user: {identifier: string, password: string}): Promise<any> {
        const authStore = useAuthStore()
        const loginData: LoginData = {...user}
        return axios
        .post(API_URL+'/oauth/token',loginData).then(response=>{
            if (response.data.access_token){
            localStorage.setItem('accessToken',response.data.access_token);
            authStore.loadTokenFromLocalStorage('accessToken')
        }
        return response.data;
    });
    }

    logout(): void {
        localStorage.removeItem('user');
    }

    register(user: {username: string, email: string, password: string}): Promise<any> {
        return axios.post(API_URL + '/users/register',{
            email: user.email,
            username: user.username,
            password: user.password,
        })
    }

}
export default new AuthService();
