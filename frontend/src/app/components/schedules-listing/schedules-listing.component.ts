import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { ScheduleDetailModel } from '../schedule-detail/schedule-detail.component';

interface ScheduleRow {
  id: number;
  startDate: string; // ISO: "2024-08-21"
  startTime: string; // "09:00"
  endDate: string; // ISO
  endTime: string; // "11:00"
  cohort: string; // "Spring 2024"
  subGroup: string; // "Group A"
  program: { id: number; name: string }; // linked program
}

@Component({
  selector: 'app-schedules-listing',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './schedules-listing.component.html',
  styleUrls: ['./schedules-listing.component.scss'],
})
export class SchedulesListingComponent implements OnInit {
  loading = true;
  rows: ScheduleRow[] = [];
  selected: ScheduleDetailModel | null = null;
  page = 1;
  size = 100;
  total: number | null = null;

  constructor(private router: Router) {}

  ngOnInit() {
    this.load();
  }

  load() {
    this.loading = true;
    const url = `http://docker.internal.host:7860/api/schedules?page=${this.page}&size=${this.size}`;
    fetch(url)
      .then((r) => r.json())
      .then((data: any) => {
        if (Array.isArray(data)) {
          this.rows = data as ScheduleRow[];
          this.total = null;
        } else if (data && Array.isArray(data.items)) {
          this.rows = data.items as ScheduleRow[];
          this.total = typeof data.total === 'number' ? data.total : null;
        } else {
          this.rows = [];
          this.total = null;
        }
      })
      .finally(() => (this.loading = false));
  }

  trackById(_: number, r: ScheduleRow) {
    return r.id;
  }

  // Optional formatter if you want to adjust display later
  fmt(date: string, time: string) {
    return `${date} at ${time}`;
  }

  openDetail(r: ScheduleRow, tab: 'details' | 'periods' = 'details') {
    // Option A: just the id + tab in query params
    this.router.navigate(['/schedules', r.id], {
      queryParams: { tab },
      // Option B: pass a snapshot so detail can render instantly (optional)
      state: { schedule: r },
    });
  }

  // Pagination helpers
  get hasPrev() {
    return this.page > 1;
  }
  get hasNext() {
    return this.total == null
      ? this.rows.length === this.size
      : this.page * this.size < this.total;
  }
  get totalPages(): number | null {
    return this.total == null
      ? null
      : Math.max(1, Math.ceil(this.total / this.size));
  }
  nextPage() {
    if (!this.hasNext) return;
    this.page++;
    this.load();
  }
  prevPage() {
    if (!this.hasPrev) return;
    this.page--;
    this.load();
  }
  changeSize(val: string | number) {
    const n = Number(val);
    if (!Number.isFinite(n) || n <= 0) return;
    this.size = n;
    this.page = 1;
    this.load();
  }
}
