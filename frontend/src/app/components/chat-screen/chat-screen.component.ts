import {AfterViewInit, Component, ElementRef, EventEmitter, Output, ViewChild} from '@angular/core';
import {CommonModule, Location} from '@angular/common';
import {Router} from '@angular/router';
import {FormsModule} from '@angular/forms';

type MsgType = 'user' | 'ai';

interface Message {
  id: string;
  type: MsgType;
  content: string;
  time: string;
}

@Component({
  selector: 'app-chat-screen',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-screen.component.html',
  styleUrls: ['./chat-screen.component.scss']
})
export class ChatScreenComponent implements AfterViewInit {
  @Output() close = new EventEmitter<void>();

  @ViewChild('messagesScroller') messagesScroller!: ElementRef<HTMLDivElement>;
  inputValue = '';

  messages: Message[] = [
    {
      id: 'm1',
      type: 'ai',
      content:
        "Hello! I'm your AI Schedule Organizer assistant. I can help you manage schedules, resolve conflicts, and make recommendations. How can I assist you today?",
      time: '2:30 PM'
    }
  ];

  constructor(private location: Location, private router: Router) {}

  ngAfterViewInit() {
    this.scrollToBottom();
  }

  private scrollToBottom() {
    // Defer to allow DOM to paint
    queueMicrotask(() => {
      const el = this.messagesScroller?.nativeElement;
      if (el) el.scrollTop = el.scrollHeight;
    });
  }

  back() {
    // Prefer going back to the previous route if available
    // Otherwise emit close (if you’re showing this inside a parent container)
    if (window.history.length > 1) {
      this.location.back();
    } else {
      this.close.emit();
      // or fallback route:
      // this.router.navigate(['/users']);
    }
  }

  send() {
    const text = this.inputValue.trim();
    if (!text) return;

    const now = new Date();
    const time = now.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });

    // user message
    this.messages.push({
      id: String(now.getTime()),
      type: 'user',
      content: text,
      time
    });
    this.inputValue = '';
    this.scrollToBottom();

    // fake AI reply (replace with real call)
    setTimeout(() => {
      this.messages.push({
        id: String(Date.now() + 1),
        type: 'ai',
        content:
          "Got it! I'll help with that. Share any constraints (cohort, room, or conflicts) and I’ll propose a schedule.",
        time: new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })
      });
      this.scrollToBottom();
    }, 800);
  }

  onKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      this.send();
    }
  }
}
