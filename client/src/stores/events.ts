import { defineStore } from "pinia";
import axios from "axios";
import { API_URL } from "@/utils/config";
import {ref} from 'vue';
import type {Socket} from 'socket.io-client';

type EventCreate = {
  title: String;
  start: String;
  end: String;
};

type Event = EventCreate & { id: Number; owner_id: Number };

import { useAuthStore } from "./auth";

export const useEventStore = defineStore('event',()=>{
  const events = ref<Event[]>([]);
  const currentEvent = ref<Event> ({})
  const authStore = useAuthStore();

    async function fetchEvents() {
      const config = {
        headers: {
          Authorization: `Bearer ${authStore.getAccessToken}`,
        },
      };
      try {
        const response = await axios.get(API_URL + "/events", config);
        if (response.status!==200)
          throw new Error(`Cannot fetch events. Error code: ${response.status}`);
        events.value = response.data;
      } catch (error) {
        throw error
      }
    }

    function setCurrentEvent (event: Event){
      currentEvent.value = event
    }

    async function createEvent(event: EventCreate) {
      const config = {
        headers: {
          Authorization: `Bearer ${authStore.getAccessToken}`,
        },
      };
      try {
        const response = await axios.post(API_URL + "/events", event, config);
        if (response.status !== 200)
          throw new Error(
            `Cannot create new event. Error code: ${response.status}`
          );
        return response.data;
      } catch (error) {
        throw error;
      }
    }

    async function updateEvent(event: Event) {
      const config = {
        headers: {
          Authorization: `Bearer ${authStore.getAccessToken}`,
        },
      };
      await axios.put(`${API_URL}/events/${event.id}`, event, config);
      const index = events.value.findIndex((e: { id: Number; }) => e.id === event.id);
      if (index !== -1) {
        events.value.splice(index, 1, event);
      }
    }

    async function deleteEvent(eventId: number) {
      const config = {
        headers: {
          Authorization: `Bearer ${authStore.getAccessToken}`,
        },
      };
      try{
        const response = await axios.delete(`${API_URL}/events/${eventId}`, config);
        return response.data
      }
      catch(error){
        throw error
      }

    }

    function addEvent(event: Event){
      events.value.push(event);
    }

    function removeEvent(_event: Event){
      events.value = events.value.filter((event: { id: number; }) => event.id !== _event.id);
    }

    function register(socket: any, event: string, action: (...args: any[])=> void){
      socket.on(event, action)
    }

    return { events, currentEvent, fetchEvents, setCurrentEvent, createEvent, updateEvent, deleteEvent, addEvent, register, removeEvent }
})

export default useEventStore;
