import io from "socket.io-client";
import { API_URL } from "./config";
import { userItemStore } from "@/stores/items";
import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore()
class Socket {
  static instance: any = null;
  private socket: any;
  private itemStore: any;
  constructor(){
    this.socket = io(API_URL, { path: '/sio/socket/', auth: { token: authStore.getAccessToken } });
    this.itemStore = userItemStore();
  }
  static getInstance() {
    if(!Socket.instance){
        Socket.instance = new Socket();
    }
    return Socket.instance;
  }
  start(){
    this.socket.on('connect', () => {
        console.log('Connected to server');
    });
    this.socket.on('disconnect', () => {
        console.log('Disconnected from server');
    });
    this.socket.on('new_message', (data) => {
        console.log('Received new message:', data);
    });
    this.socket.on('new_item', (item)=>{
        console.log('Add new item:', item)
        this.itemStore.items.push(item)
    })
  }
  emit(event: string, data: Record<string,any>){
    this.socket.emit(event, data);
  }
  disconnect(){
    this.socket.disconnect();
  }
}

export const socket = Socket.getInstance()
