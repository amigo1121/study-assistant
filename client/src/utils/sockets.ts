import io from "socket.io-client";
import type { Socket } from "socket.io-client";
import { API_URL } from "./config";
import { useAuthStore } from "@/stores/auth";

type EventHandler = (data: any) => void;

export class BaseSocket {
  static instance: BaseSocket | null = null;

  private socket: Socket;

  constructor(token: string) {
    this.socket = io(API_URL, {
      path: "/sio/socket/",
      auth: { token },
    });
    this.socket.on("connect", () => {
      console.log("Connected to server");
    });
    this.socket.on("disconnect", () => {
      console.log("Disconnected from server");
    });
  }

  static getInstance(token: string): BaseSocket {
    if (!BaseSocket.instance) {
      BaseSocket.instance = new BaseSocket(token);
    }
    return BaseSocket.instance;
  }

  emit(event: string, data: Record<string, any>) {
    this.socket.emit(event, data);
  }

  on(event: string, handler: EventHandler) {
    this.socket.on(event, handler);
  }

  disconnect() {
    this.socket.disconnect();
  }
  protected subscribe(
    event: string,
    handle: (data: Record<string, any>) => void
  ) {
    this.socket.on(event, (data) => handle(data));
  }
}

export default BaseSocket
