import axios from 'axios';
import jwtDecode from 'jwt-decode';

const API_URL = 'http://localhost';

class AuthService {
    login(user: {identifier: string, password: string}): Promise<any> {
        return axios
        .post(API_URL+'/users/login',{
            userIdentifier: user.identifier,
            password: user.password,
        }).then(response=>{if (response.data.accessToken){
            localStorage.setItem('user',JSON.stringify(response.data));
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


    getCurrentUser(): any {
        const user = localStorage.getItem('user');
        if (user){
            return JSON.parse(user);
        }
    }

    getToken(){
        const user = this.getCurrentUser();
        if (user && user.accessToken){
            const decodedToken: any = jwtDecode(user.accessToken);
            const currentDate = new Date ();

            if (decodedToken.exp * 1000 < currentDate.getTime()){
                this.logout();
                window.location.reload();
            }
            else {
                return user.accessToken;
            }
        }
        return null;
    }
}
export default new AuthService();
