import { defineStore } from "pinia";
import axios from "axios";
import { API_URL } from "@/utils/config";
import {ref} from 'vue';
import type {Socket} from 'socket.io-client';

type EventCreate = {
  title: string;
  start: string;
  end: string;
};

type Event = EventCreate & { id: number; owner_id?: number };

type EventUpdate ={
  title?: string
  start?: string
  end?: string
  id: number
}

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

    async function updateEvent(event: EventUpdate) {
      const config = {
        headers: {
          Authorization: `Bearer ${authStore.getAccessToken}`,
        },
      };
      const {id,..._event} = event
      await axios.put(`${API_URL}/events/${event.id}`, _event, config);

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
      const index = events.value.findIndex((e: { id: number; }) => e.id === _event.id);
      if (index !== -1) {
        events.value.splice(index, 1);
      }
    }

    function modifyEvent(event: Event){
      const index = events.value.findIndex((e: { id: number; }) => e.id === event.id);
      if (index !== -1) {
        events.value.splice(index, 1, event);
      }
    }

    function register(socket: any, event: string, action: (...args: any[])=> void){
      socket.on(event, action)
    }

    return { events, currentEvent, fetchEvents, setCurrentEvent, createEvent, updateEvent, deleteEvent, addEvent, register, removeEvent, modifyEvent }
})

export default useEventStore;
