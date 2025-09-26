import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

type CohortStatus = 'Active' | 'Completed' | 'Upcoming' | 'Planning';

interface CohortRow {
  name: string; // "Spring 2024"
  subgroups: string[]; // ["A1", "A2"] or []
  status?: CohortStatus; // pill (optional; backend may not provide)
}

@Component({
  selector: 'app-cohorts-listing',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cohorts-listing.component.html',
  styleUrls: ['./cohorts-listing.component.scss'],
})
export class CohortsListingComponent implements OnInit {
  loading = true;
  rows: CohortRow[] = [];
  page = 1;
  size = 100;
  total: number | null = null;

  ngOnInit() {
    this.load();
  }

  load() {
    this.loading = true;
    const url = `/api/cohorts?page=${this.page}&size=${this.size}`;
    fetch(url)
      .then((r) => r.json())
      .then((data: any) => {
        let items: any[] = [];
        if (Array.isArray(data)) {
          items = data;
          this.total = null;
        } else if (data && Array.isArray(data.items)) {
          items = data.items;
          this.total = typeof data.total === 'number' ? data.total : null;
        } else {
          this.total = null;
        }

        // Normalize each item so subgroups becomes string[] of names
        this.rows = items.map((raw: any) => {
          const rawSubs = raw?.subgroups;
          let subgroups: string[] = [];
          if (Array.isArray(rawSubs)) {
            subgroups = rawSubs.map((sg: any) =>
              typeof sg === 'string' ? sg : sg?.name ?? String(sg)
            );
          } else if (rawSubs && typeof rawSubs === 'object') {
            // Single object case
            subgroups = [rawSubs.name ?? String(rawSubs)];
          }
          const row: CohortRow = {
            name: raw?.name ?? '',
            subgroups,
            status: raw?.status as CohortStatus | undefined,
          };
          return row;
        });
      })
      .finally(() => (this.loading = false));
  }

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

  trackByName(_: number, r: CohortRow) {
    return r.name;
  }
}
