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
  constructor() { }

  public connect(): void {
    if (!this.socket$ || this.socket$.closed) {
      this.socket$ = webSocket(URL);

      this.socket$.subscribe((data: Message | any) => {
        if (data["hi"]) {
          this.id = data["hi"]
          console.log(this.id)
        }
        else
          this.msgs.push(data)
      });
    }
  }

  sendMessage(message: string) {
    this.socket$.next({ "action": "msg", "msg": message });
  }

  close() {
    this.socket$.complete();
  }
}
