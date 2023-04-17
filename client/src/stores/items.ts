import { defineStore } from "pinia";
import axios from "axios";
import { API_URL } from "@/utils/config";
import { useAuthStore } from "./auth";

type Item = {
  content: string;
};

const authStore = useAuthStore();

export const userItemStore = defineStore({
  id: "item",
  state: () => {
    return {
      items: [] as Item[],
      currentItem: {} as Item,
    };
  },
  actions: {
    async fetchItems() {
      const config = {
        headers: {
          Authorization: `Bearer ${authStore.getAccessToken}`,
        },
      };
      const response = await axios.get(API_URL + "/items", config);
      this.items = response.data;
    },
    setCurrentItem(item) {
      this.currentItem = item;
    },
    async addItem(item) {
      const config = {
        headers: {
          Authorization: `Bearer ${authStore.getAccessToken}`,
        },
      };
      return await axios.post(API_URL + "/items", item, config);
    },
    async deleteItem(itemId) {
      await axios.delete(`${API_URL}/items/${itemId}`);
      this.items = this.items.filter((item) => item.id !== itemId);
    },
  },
});
