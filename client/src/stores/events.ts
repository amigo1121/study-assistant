import { defineStore } from "pinia";
import axios from "axios";
import { API_URL } from "@/utils/config";
import { useAuthStore } from "./auth";

type EventCreate = {
  title: String;
  start: String;
  end: String;
};

type Event = EventCreate & { id: Number, owner_id: Number };

const authStore = useAuthStore();
let todayStr = new Date().toISOString().replace(/T.*$/, '')
export const useEventStore = defineStore({
  id: "event",
  state: () => {
    return {
      events: [
        {
          id: 99,
          owner_id: 60,
          title: "Timed event",
          start: todayStr + "T12:00:00",
          end: todayStr + "T20:00:00",
        },
      ] as Event[],
      currentEvent: {} as Event,
    };
  },
  actions: {
    async fetchEvents() {
      const config = {
        headers: {
          Authorization: `Bearer ${authStore.getAccessToken}`,
        },
      };
      const response = await axios.get(API_URL + "/events", config);
      this.events = response.data;
    },
    setCurrentEvent(event: Event) {
      this.currentEvent = event;
    },
    async createEvent(event: EventCreate) {
      const config = {
        headers: {
          Authorization: `Bearer ${authStore.getAccessToken}`,
        },
      };
      const response = await axios.post(API_URL + "/events", event, config);
      this.events.push(response.data);
      return response.data
    },
    async updateEvent(event: Event) {
      const config = {
        headers: {
          Authorization: `Bearer ${authStore.getAccessToken}`,
        },
      };
      await axios.put(`${API_URL}/events/${event.id}`, event, config);
      const index = this.events.findIndex((e) => e.id === event.id);
      if (index !== -1) {
        this.events.splice(index, 1, event);
      }
    },
    async deleteEvent(eventId: number) {
      const config = {
        headers: {
          Authorization: `Bearer ${authStore.getAccessToken}`,
        },
      };
      console.log(eventId);
      await axios.delete(`${API_URL}/events/${eventId}`, config);
      this.events = this.events.filter((event) => event.id !== eventId);
    },
  },
});

export default useEventStore;
