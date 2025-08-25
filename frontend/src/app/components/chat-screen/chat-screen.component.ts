import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-chat-screen',
  imports: [],
  templateUrl: './chat-screen.component.html',
  styleUrl: './chat-screen.component.scss'
})
export class ChatScreenComponent {
  @Output() close = new EventEmitter<void>();

  onClose() {
    this.close.emit();
  }
}
