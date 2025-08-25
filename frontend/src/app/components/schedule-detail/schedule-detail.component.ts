import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-schedule-detail',
  imports: [],
  templateUrl: './schedule-detail.component.html',
  standalone: true,
  styleUrl: './schedule-detail.component.scss'
})
export class ScheduleDetailComponent {
  @Output() back = new EventEmitter<void>();

  onBack() {
    this.back.emit();
  }
}
