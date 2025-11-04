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
  sessionId: string;

  messages: Message[] = [
    {
      id: 'm1',
      type: 'ai',
      content:
        "Hello! I'm your AI Schedule Organizer assistant. I can help you manage schedules, resolve conflicts, and make recommendations. How can I assist you today?",
      time: '2:30 PM',
    },
  ];

  constructor(private location: Location, private router: Router) {
    // Retrieve or create a persistent sessionId from localStorage
    const storedSessionId = localStorage.getItem('chatSessionId');
    if (storedSessionId) {
      this.sessionId = storedSessionId;
      console.log('Restored session:', this.sessionId);
    } else {
      this.sessionId = uuidv4();
      localStorage.setItem('chatSessionId', this.sessionId);
      console.log('Created new session:', this.sessionId);
    }
  }

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

    try {
      const res = await fetch('/api/prompt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt,
          sessionId: this.sessionId,
        }),
      });

      console.log('Response status:', res.status);

      if (!res.ok) {
        const errorText = await res.text();
        console.error('Response error:', errorText);
        throw new Error(`${res.status} ${res.statusText}: ${errorText}`);
      }

      let data: any = null;
      try {
        data = await res.json();
        console.log('Response data:', data);
      } catch (err) {
        console.error('Failed to parse JSON:', err);
        data = null;
      }

      // Use the utility function to extract text from any response format
      let reply = '';

      if (data && data.n8n_response) {
        reply = this.extractTextFromResponse(data.n8n_response);
      } else if (data) {
        reply = this.extractTextFromResponse(data);
      }

      console.log('Final reply:', reply);

      // Check if we got empty or invalid response
      if (!reply || reply.trim() === '' || reply === '{}' || reply === '[]') {
        console.warn('Empty response detected, full data:', data);
        reply = 'Received empty response from AI. Please try again.';
      }

      this.pushAiMessage(reply);
    } catch (err) {
      console.error('Send error:', err);
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

  /**
   * Recursively extract text content from various n8n response formats
   */
  private extractTextFromResponse(data: any): string {
    // Handle null/undefined
    if (!data) return '';

    // Handle string
    if (typeof data === 'string') return data;

    // Handle array - try to extract text from each item
    if (Array.isArray(data)) {
      return data
        .map((item) => this.extractTextFromResponse(item))
        .filter((text) => text.trim() !== '')
        .join('\n\n');
    }

    // Handle object - try common text field names
    if (typeof data === 'object') {
      // Priority order for text fields
      const textFields = [
        'description',
        'text',
        'message',
        'output',
        'response',
        'result',
        'content',
        'body',
        'data',
      ];

      for (const field of textFields) {
        if (data[field]) {
          const extracted = this.extractTextFromResponse(data[field]);
          if (extracted) return extracted;
        }
      }

      // If no known field found, stringify but try to make it readable
      try {
        const stringified = JSON.stringify(data, null, 2);
        // Don't return empty objects
        if (stringified === '{}' || stringified === '[]') return '';
        return stringified;
      } catch {
        return String(data);
      }
    }

    // Fallback
    return String(data);
  }

  /**
   * Reset the chat session (for debugging or starting fresh)
   * This creates a new sessionId and clears the localStorage
   */
  resetSession() {
    this.sessionId = uuidv4();
    localStorage.setItem('chatSessionId', this.sessionId);
    this.messages = [
      {
        id: 'm1',
        type: 'ai',
        content:
          "Hello! I'm your AI Schedule Organizer assistant. I can help you manage schedules, resolve conflicts, and make recommendations. How can I assist you today?",
        time: new Date().toLocaleTimeString([], {
          hour: 'numeric',
          minute: '2-digit',
        }),
      },
    ];
    console.log('Session reset:', this.sessionId);
  }
}
