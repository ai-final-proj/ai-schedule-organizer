import { Component, EventEmitter, Input, Output, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {ActivatedRoute, Router} from '@angular/router';

export interface ScheduleDetailModel {
  id: number;
  title: string;
  cohort: string;
  subGroup: string;
  startDate: string; // ISO 'YYYY-MM-DD'
  startTime: string; // 'HH:mm'
  endDate: string;
  endTime: string;
  program?: { id: number; name: string }; // optional
}

export interface PeriodRow {
  id: number;
  name: string;
  instructor: string;
  startDate: string;
  startTime: string;
  endDate: string;
  endTime: string;
}

@Component({
  selector: 'app-schedule-detail',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './schedule-detail.component.html',
  styleUrls: ['./schedule-detail.component.scss'],
})
export class ScheduleDetailComponent implements OnInit {
  @Input({ required: true }) schedule!: ScheduleDetailModel;
  @Input() periods: PeriodRow[] | null = null;
  @Output() back = new EventEmitter<void>();

  activeTab: 'details'|'periods' = 'details';
  id!: number;

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit() {
    // 1) read id
    this.id = Number(this.route.snapshot.paramMap.get('id'));

    // 2) set tab from query param (default = 'details')
    const qpTab = (this.route.snapshot.queryParamMap.get('tab') ?? 'details') as 'details'|'periods';
    this.activeTab = qpTab;

    // 3) if no @Input schedule, try to use navigation state; otherwise fetch by id
    if (!this.schedule) {
      const st = history.state?.schedule as ScheduleDetailModel | undefined;
      if (st && st.id === this.id) {
        this.schedule = {
          id: st.id,
          title: st['title'] ?? 'Scheduled Session', // fallback if list had no title
          cohort: st.cohort,
          subGroup: st.subGroup,
          startDate: st.startDate, startTime: st.startTime,
          endDate: st.endDate,     endTime: st.endTime,
          program: st.program
        };
      } else {
        // TODO: fetch schedule + periods by this.id
        // For now, synthesize a minimal object so UI renders.
        this.schedule = {
          id: this.id,
          title: 'Scheduled Session',
          cohort: 'TBD', subGroup: 'TBD',
          startDate: '—', startTime: '—',
          endDate: '—',   endTime: '—'
        };
      }
    }
    if (!this.periods) {
      // fallback demo periods – replace with fetch by schedule.id
      this.periods = [
        { id: 1, name: 'Opening Session',   instructor: 'Bob Smith', startDate: '2024-08-21', startTime: '09:00', endDate: '2024-08-21', endTime: '09:15' },
        { id: 2, name: 'Python Basics',     instructor: 'Bob Smith', startDate: '2024-08-21', startTime: '09:15', endDate: '2024-08-21', endTime: '10:00' },
        { id: 3, name: 'Hands-on Exercise', instructor: 'Bob Smith', startDate: '2024-08-21', startTime: '10:15', endDate: '2024-08-21', endTime: '10:45' },
        { id: 4, name: 'Q&A Session',       instructor: 'Bob Smith', startDate: '2024-08-21', startTime: '10:45', endDate: '2024-08-21', endTime: '11:00' },
      ];
    }
  }

  goBack() {
    // Prefer going back to the listing route
    this.router.navigate(['/schedules']);
    // Or emit for parent-controlled navigation:
    // this.back.emit();
  }
  setTab(tab: 'details' | 'periods') { this.activeTab = tab; }

  fmt(date: string, time: string) { return `${date} at ${time}`; }
}
