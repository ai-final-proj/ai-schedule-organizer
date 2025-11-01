import { AfterViewInit, Component, ElementRef, EventEmitter, Output, ViewChild } from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

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
  sending = false;

  private readonly webhookUrl =
    'http://http://35.224.46.46:5678/webhook-test/38cf2c4a-eb7a-4a66-970c-2c734a53b552';
  private readonly sessionId = '4e1a7686b6694a5e9d45b878f271233a';

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
    if (this.sending) return;
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
    // Call backend API which forwards the prompt to n8n and returns results
    (async () => {
      try {
        const res = await fetch('/api/prompt', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt: text })
        });
        let data: any = null;
        try { data = await res.json(); } catch (e) { data = { text: await res.text() }; }

        // Prefer a human-friendly text field if available, otherwise stringify
        let reply = '';
        if (data && data.n8n_response) {
          if (typeof data.n8n_response === 'string') reply = data.n8n_response;
          else if (data.n8n_response.text) reply = data.n8n_response.text;
          else reply = JSON.stringify(data.n8n_response);
        } else if (data && data.text) {
          reply = data.text;
        } else {
          reply = 'No response from n8n.';
        }

        this.messages.push({
          id: String(Date.now() + 1),
          type: 'ai',
          content: reply,
          time: new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })
        });
        this.scrollToBottom();
      } catch (err) {
        this.messages.push({
          id: String(Date.now() + 2),
          type: 'ai',
          content: 'Error contacting server: ' + String(err),
          time: new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })
        });
        this.scrollToBottom();
      }
    })();
  }

  onKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      this.send();
    }
  }

  private async postToWebhook(chatInput: string) {
    this.sending = true;
    const payload = [
      {
        sessionId: this.sessionId,
        action: 'sendMessage' as const,
        chatInput
      }
    ];

    try {
      const response = await fetch(this.webhookUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      let aiContent: string;

      if (!response.ok) {
        aiContent = `Workflow error: ${response.status} ${response.statusText}`;
      } else {
        aiContent = await this.parseWorkflowResponse(response);
      }

      this.pushAiMessage(aiContent);
    } catch (error) {
      console.error('Failed to send chat payload to n8n webhook', error);
      const message =
        error instanceof Error ? error.message : 'Unexpected error while calling the webhook.';
      this.pushAiMessage(`Sorry, I couldn't reach the workflow. ${message}`);
    } finally {
      this.sending = false;
      this.scrollToBottom();
    }
  }

  private async parseWorkflowResponse(response: Response): Promise<string> {
    const contentType = response.headers.get('content-type') ?? '';

    try {
      if (contentType.includes('application/json')) {
        const data = await response.json();
        return this.formatResponseMessage(data);
      }

      const text = await response.text();
      if (text.trim().length === 0) {
        return 'Workflow accepted the message.';
      }

      return `Workflow response: ${text}`;
    } catch (error) {
      console.warn('Unable to read webhook response body', error);
      return 'Workflow accepted the message.';
    }
  }

  private formatResponseMessage(data: unknown): string {
    if (data == null) {
      return 'Workflow accepted the message.';
    }

    if (typeof data === 'string') {
      return data;
    }

    if (typeof data === 'object') {
      const record = data as Record<string, unknown>;
      const fallbackKeys = ['message', 'result', 'response', 'status'];

      for (const key of fallbackKeys) {
        const value = record[key];
        if (typeof value === 'string' && value.trim().length > 0) {
          return value;
        }
      }

      try {
        return `Workflow response: ${JSON.stringify(data)}`;
      } catch {
        return 'Workflow accepted the message.';
      }
    }

    return `Workflow response: ${String(data)}`;
  }

  private pushAiMessage(content: string) {
    const now = new Date();
    this.messages.push({
      id: `${now.getTime()}-ai`,
      type: 'ai',
      content,
      time: now.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })
    });
  }
}
