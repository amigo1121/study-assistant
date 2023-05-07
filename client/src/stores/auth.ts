import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";
import { API_URL, refreshTokenIntervalInMinutes } from "@/utils/config";

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
      role: null,
      first_name: null,
      last_name: null,
      timeoutID: null,
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
        const response = await axios.get(
          API_URL + "/oauth/refreshtoken",
          config
        );
        if (response.status === 200) {
          const data = await response.data;
          localStorage.setItem("accessToken", data.access_token);
          this.loadTokenFromLocalStorage("accessToken");
          console.log("Refresh token success");
          this.timeoutID = setTimeout(
            this.tryRefreshToken,
            refreshTokenIntervalInMinutes * 60 * 1000
          );
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
      let config = {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      };
      try {
        const response = await axios.get(API_URL + "/oauth/authorize", config);
        if (response.status !== 200) {
          throw new Error("Failed to authenticate with access token");
        }
        console.log("Authenticate successful");
        this.setInfor(response.data);
        if (this.timeoutID) {
          console.log("continue loading");
        } else {
          console.log("welcome back");
          if (this.refreshToken) await this.tryRefreshToken();
        }
        return response;
      } catch (error) {
        console.error(error);
        try {
          await this.tryRefreshToken();
          config = {
            headers: {
              Authorization: `Bearer ${this.accessToken}`,
            },
          };
          const response = await axios.get(
            API_URL + "/oauth/authorize",
            config
          );
          if (response.status !== 200) {
            throw new Error(
              "Failed to authenticate with refreshed access token"
            );
          }
          this.setInfor(response.data);
          console.log("Authenticate successful with refreshed access token");
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
    setRole(role: String) {
      this.role = role;
    },
    setInfor(data) {
      this.username = data.username;
      this.first_name = data.first_name;
      this.last_name = data.last_name;
      this.email = data.email;
      this.role = data.role;
    },
    clearToken() {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      localStorage.removeItem("loginTime");
    },
    resetData() {
      this.accessToken = null;
      this.refreshToken = null;
      this.username = null;
      this.email = null;
      this.role = null;
      this.first_name = null;
      this.last_name = null;
      this.timeoutID = null;
    },
    logout() {
      this.clearToken();
      this.resetData();
      router.go();
    },
    async login(
      user: { identifier: string; password: string },
      isRemember: boolean
    ): Promise<any> {
      const authStore = useAuthStore();
      const loginData: LoginData = { ...user };
      return axios
        .post(API_URL + "/oauth/token", loginData)
        .then((response) => {
          if (response.data.access_token) {
            localStorage.setItem("accessToken", response.data.access_token);
            authStore.loadTokenFromLocalStorage("accessToken");
            localStorage.setItem("loginTime", new Date().toUTCString());
          }
          if (isRemember && response.data.refresh_token) {
            localStorage.setItem("refreshToken", response.data.refresh_token);
            authStore.loadTokenFromLocalStorage("refreshToken");
            this.timeoutID = setTimeout(
              this.tryRefreshToken,
              refreshTokenIntervalInMinutes * 60 * 1000
            );
          }
          return response.data;
        });
    },
    async register(user: {
      username: string;
      email: string;
      password: string;
      code: string;
      first_name: string;
      last_name: string;
    }): Promise<any> {
      return axios.post(API_URL + "/users/register", user);
    },
    async changePassword(data: { old_password: string; new_password: string }) {
      const config = {
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
        },
      };
      return axios.post(API_URL + "/users/changepw", data, config);
    },
  },
});
