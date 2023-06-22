import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Message } from '../model/message';

const URL = "ws://localhost:9001"
const subject = webSocket(URL);

@Injectable({
  providedIn: 'root'
})
export class MessageService {
  private socket$!: WebSocketSubject<any>;
  public msgs: Message[] = [];
  public id = ""
  public counter: number = 1
  constructor() { }

  public connect(): void {
    if (!this.socket$ || this.socket$.closed) {
      this.socket$ = webSocket(URL);

      this.socket$.subscribe((data: Message | any) => {
        if (data["hi"]) {
          this.counter = data["connected"]
          this.id = data["hi"]
          this.counter
        } else if (data["join"]) {
          this.counter = data["connected"]
          this.msgs.push({
            mine: 0,
            sender: "server",
            msg: data["join"] + " join the chat",
            admin: "0"
          })
        } else if (data["left"]) {
          this.counter = data["connected"]
          this.msgs.push({
            mine: 0,
            sender: "server",
            msg: data["left"] + " left the chat",
            admin: "0"
          })
        } else {
          let mine = data["sender"] == this.id ? 1 : 2;
          this.msgs.push({
            mine: mine,
            sender: data["sender"],
            msg: data["msg"],
            admin: data["admin"]
          })
        }
      });
    }
  }

  sendMessage(message: string) {
    this.socket$.next({ "admin": "0", "action": "msg", "msg": message });
  }

  close() {
    this.socket$.complete();
  }
}
