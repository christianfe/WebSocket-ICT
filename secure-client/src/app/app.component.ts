import { Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { Message } from './model/message';
import { MessageService } from './service/message.service';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {
  @ViewChild('messageForm') messageForm?: NgForm
  messages: Message[] = []
  m = '';
  constructor(public messageService: MessageService) {
  }
  ngOnDestroy(): void {
    this.messageService.close()
  }
  ngOnInit() {
    this.messageService.connect()
  }
  send(message: string) {
    if (message)
      this.messageService.sendMessage(message);
    this.m = '';
  }

}
