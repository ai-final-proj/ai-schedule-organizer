import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {Router, RouterLink} from '@angular/router';
import {ScheduleDetailModel} from '../schedule-detail/schedule-detail.component';

interface ScheduleRow {
  id: number;
  startDate: string;  // ISO: "2024-08-21"
  startTime: string;  // "09:00"
  endDate: string;    // ISO
  endTime: string;    // "11:00"
  cohort: string;     // "Spring 2024"
  subGroup: string;   // "Group A"
  program: { id: number; name: string }; // linked program
}

@Component({
  selector: 'app-schedules-listing',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './schedules-listing.component.html',
  styleUrls: ['./schedules-listing.component.scss']
})
export class SchedulesListingComponent implements OnInit {
  loading = true;
  rows: ScheduleRow[] = [];
  selected: ScheduleDetailModel | null = null;

  constructor(private router: Router) {}

  ngOnInit() {
    // TODO: replace with real fetch
    // fetch('/api/schedules').then(r => r.json()).then((data: ScheduleRow[]) => { this.rows = data; this.loading = false; });
    setTimeout(() => {
      this.rows = [
        {
          id: 1,
          startDate: '2024-08-21', startTime: '09:00',
          endDate:   '2024-08-21', endTime:   '11:00',
          cohort: 'Spring 2024', subGroup: 'Group A',
          program: { id: 101, name: 'Data Science Bootcamp' }
        },
        {
          id: 2,
          startDate: '2024-08-21', startTime: '14:00',
          endDate:   '2024-08-21', endTime:   '17:00',
          cohort: 'Spring 2024', subGroup: 'Group B',
          program: { id: 101, name: 'Data Science Bootcamp' }
        },
        {
          id: 3,
          startDate: '2024-08-22', startTime: '10:00',
          endDate:   '2024-08-22', endTime:   '12:00',
          cohort: 'Spring 2024', subGroup: 'Group A',
          program: { id: 101, name: 'Data Science Bootcamp' }
        },
        {
          id: 4,
          startDate: '2024-08-23', startTime: '13:00',
          endDate:   '2024-08-23', endTime:   '16:00',
          cohort: 'Fall 2023', subGroup: 'All Groups',
          program: { id: 202, name: 'Web Development' }
        },
        {
          id: 5,
          startDate: '2024-08-24', startTime: '15:00',
          endDate:   '2024-08-24', endTime:   '16:30',
          cohort: 'Summer 2024', subGroup: 'Group C',
          program: { id: 303, name: 'UX/UI Design' }
        },
      ];
      this.loading = false;
    }, 350);
  }

  trackById(_: number, r: ScheduleRow) { return r.id; }

  // Optional formatter if you want to adjust display later
  fmt(date: string, time: string) { return `${date} at ${time}`; }

  openDetail(r: ScheduleRow, tab: 'details'|'periods' = 'details') {
    // Option A: just the id + tab in query params
    this.router.navigate(['/schedules', r.id], {
      queryParams: { tab },
      // Option B: pass a snapshot so detail can render instantly (optional)
      state: { schedule: r }
    });
  }
}
