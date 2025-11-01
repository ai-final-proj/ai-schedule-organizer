import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ScheduleDetailModel } from '../schedule-detail/schedule-detail.component';

interface ScheduleRow {
  id: number;
  name: string;
  description?: string | null;
  cohort?: string | null;
  subgroup?: string | null;
  program?: { id: number; name: string } | null;
}

@Component({
  selector: 'app-schedules-listing',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './schedules-listing.component.html',
  styleUrls: ['./schedules-listing.component.scss'],
})
export class SchedulesListingComponent implements OnInit {
  loading = true;
  rows: ScheduleRow[] = [];
  selected: ScheduleDetailModel | null = null;
  page = 1;
  size = 20;
  total: number | null = null;
  error: string | null = null;

  constructor(private router: Router) {}

  ngOnInit() {
    this.load();
  }

  load() {
    this.loading = true;
    this.error = null;
    const url = `/api/schedules?page=${this.page}&size=${this.size}`;
    fetch(url)
      .then((r) => {
        if (!r.ok) console.error('GET', url, '->', r.status, r.statusText);
        return r.json();
      })
      .then((data: any) => {
        const items: any[] | null = Array.isArray(data)
          ? data
          : data && Array.isArray(data.items)
          ? data.items
          : null;

        if (!items) {
          this.rows = [];
          this.total = null;
          return;
        }

        this.rows = items.map((raw) => this.toRow(raw));
        this.total =
          data && typeof data.total === 'number' ? data.total : null;
      })
      .catch((err) => {
        console.error('Fetch schedules failed:', url, err);
        this.error = 'Unable to load schedules.';
        this.rows = [];
        this.total = null;
      })
      .finally(() => (this.loading = false));
  }

  trackById(_: number, r: ScheduleRow) {
    return r.id;
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

  private toRow(raw: any): ScheduleRow {
    return {
      id: Number(raw.id),
      name: raw.name ?? 'Untitled schedule',
      description: raw.description ?? null,
      cohort: raw.cohort ?? null,
      subgroup: raw.subgroup ?? null,
      program: raw.program
        ? { id: Number(raw.program.id), name: raw.program.name ?? 'Program' }
        : null,
    };
  }
}
