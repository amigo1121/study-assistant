import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";
import { API_URL, refreshTokenIntervalInMinutes} from "@/utils/config";

type LoginData = {
  identifier: string;
  password: string;
};
export const useAuthStore = defineStore({
  id: "auth",
  state: () => {
    return {
      accessToken: null,
      refreshToken: null,
      username: null,
      email: null,
    };
  },
  getters: {
    getAccessToken(state): string | null {
      return state.accessToken;
    },
    getRefresshToken(state): string | null {
      return state.refreshToken;
    },
  },
  actions: {
    loadTokenFromLocalStorage(tokenKey: string) {
      const accessToken = localStorage.getItem(tokenKey);
      if (accessToken) this[tokenKey] = accessToken;
    },
    async tryRefreshToken() {
      const refreshToken = this.refreshToken || "";
      const config = {
        headers: {
          Authorization: `Bearer ${refreshToken}`,
        },
      };
      try {
        const response = await axios.get(API_URL+"/oauth/refreshtoken", config);
        if (response.status === 200) {
          const data = await response.data;
          localStorage.setItem("accessToken", data.access_token)
          this.loadTokenFromLocalStorage("accessToken");
          console.log("Refresh token success")
        } else {
          throw new Error("Failed to refresh access token");
        }
        return response;
      } catch (error) {
        console.error(error);
        throw new Error("Failed to refresh access token");
      }
    },

    async tryAuthenticate() {
      const accessToken = this.accessToken || "";
      const config = {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      };
      try {
        const response = await axios.get(API_URL + "/oauth/authorize", config);
        if (response.status !== 200) {
          throw new Error("Failed to authenticate with access token");
        }
        this.setEmail(response.data.email)
        this.setUsername(response.data.username)
        console.log("Authenticate successful")
        return response;
      } catch (error) {
        console.error(error);
        try {
          await this.tryRefreshToken();
          const response = await axios.get(API_URL + "/oauth/authorize", config);
          if (response.status !== 200) {
            throw new Error("Failed to authenticate with refreshed access token");
          }
          return response;
        } catch (error) {
          console.error(error);
          throw new Error("Failed to authenticate");
        }
      }
    },

    setUsername(username: string) {
      this.username = username;
    },
    setEmail(email: string) {
      this.email = email;
    },
    logout() {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      router.go();
    },
    async login(user: { identifier: string; password: string }): Promise<any> {
      const authStore = useAuthStore();
      const loginData: LoginData = { ...user };
      return axios
        .post(API_URL + "/oauth/token", loginData)
        .then((response) => {
          if (response.data.access_token) {
            localStorage.setItem("accessToken", response.data.access_token);
            authStore.loadTokenFromLocalStorage("accessToken");
          }
          if(response.data.refresh_token){
            localStorage.setItem("refreshToken", response.data.refresh_token);
            authStore.loadTokenFromLocalStorage("refreshToken");
          }
          return response.data;
        });
    },
    async register(user: {
      username: string;
      email: string;
      password: string;
    }): Promise<any> {
      return axios.post(API_URL + "/users/register", {
        email: user.email,
        username: user.username,
        password: user.password,
      });
    },
    startRefreshToken(){
      setInterval(()=>{
        this.tryRefreshToken()
      },refreshTokenIntervalInMinutes*60*1000)
    }
  },
});
