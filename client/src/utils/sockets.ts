import type { Socket } from "socket.io-client";
import { Manager } from "socket.io-client"
import { API_URL } from "./config";

type EventHandler = (data: any) => void;

export class BaseSocket {
  static instance: BaseSocket | null = null;

  private socket: Socket;
  private manager = null;
  constructor() {
    this.manager = new Manager(API_URL,{path: "/sio/socket", autoConnect: false});
  }

  static getInstance(): BaseSocket {
    if (!BaseSocket.instance) {
      BaseSocket.instance = new BaseSocket();
    }
    return BaseSocket.instance;
  }

  emit(event: string, data: Record<string, any>) {
    this.socket.emit(event, data);
  }

  public on(event: string, handler: EventHandler) {
    this.socket.on(event, handler);
  }

  public off(event: string){
    if(this.socket)
    this.socket.off(event);
  }

  public offAll(){
    if(this.socket)
    this.socket.off();
  }

  public set(_option) {
    this.socket = this.manager.socket("/", _option);

    // this.manager = new Manager(API_URL, {autoConnect: false});
    // this.socket = io(API_URL, {
    //   path: "/sio/socket/",
    //   autoConnect: false,
    //   ..._option
    // });

    this.socket.on("connect", () => {
      console.log("Connected to server",this.socket.id);
    });

  }

  public connect() {
    this.socket.connect();
    this.socket.on("disconnect", () => {
      console.log("Disconnected from server",this.socket.id);
    });
  }

  public disconnect() {
    if (this.socket) this.socket.disconnect();
    this.socket = null;
  }

  // protected subscribe(
  //   event: string,
  //   handle: (data: Record<string, any>) => void
  // ) {
  //   this.socket.on(event, (data) => handle(data));
  // }
}

export default BaseSocket;
