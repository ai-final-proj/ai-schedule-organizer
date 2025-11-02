import {
  AfterViewInit,
  Component,
  ElementRef,
  EventEmitter,
  Output,
  ViewChild,
} from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { v4 as uuidv4 } from 'uuid';

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
  styleUrls: ['./chat-screen.component.scss'],
})
export class ChatScreenComponent implements AfterViewInit {
  @Output() close = new EventEmitter<void>();

  @ViewChild('messagesScroller') messagesScroller!: ElementRef<HTMLDivElement>;
  inputValue = '';
  sending = false;

  private readonly webhookUrl =
    'http://35.224.46.46:5678/webhook/38cf2c4a-eb7a-4a66-970c-2c734a53b552';

  messages: Message[] = [
    {
      id: 'm1',
      type: 'ai',
      content:
        "Hello! I'm your AI Schedule Organizer assistant. I can help you manage schedules, resolve conflicts, and make recommendations. How can I assist you today?",
      time: '2:30 PM',
    },
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

  async send() {
    if (this.sending) return;
    const prompt = this.inputValue.trim();
    if (!prompt) return;

    this.sending = true;
    this.addUserMessage(prompt);
    const sessionId = uuidv4();
    try {
      const payload = [
        {
          sessionId: sessionId,
          action: 'sendMessage',
          chatInput: prompt,
        },
      ];
      const res = await fetch(this.webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);

      const raw = await res.text();
      const data = raw ? JSON.parse(raw) : { text: '' };
      const reply =
        typeof data === 'string' ? data : data.text ?? JSON.stringify(data);

      this.pushAiMessage(reply);
    } catch (err) {
      this.pushAiMessage(`Webhook error: ${String(err)}`);
    } finally {
      this.sending = false;
      this.scrollToBottom();
    }
  }

  onKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      this.send();
    }
  }

  private addUserMessage(content: string) {
    const now = new Date();
    this.messages.push({
      id: `${now.getTime()}-user`,
      type: 'user',
      content,
      time: now.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }),
    });
  }

  private pushAiMessage(content: string) {
    const now = new Date();
    this.messages.push({
      id: `${now.getTime()}-ai`,
      type: 'ai',
      content,
      time: now.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }),
    });
  }
}
