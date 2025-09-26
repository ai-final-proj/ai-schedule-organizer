import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface ProgramRow {
  id: number;
  name: string;
  periods: number; // “Periods Count”
}

@Component({
  selector: 'app-programs-listing',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './programs-listing.component.html',
  styleUrls: ['./programs-listing.component.scss'],
})
export class ProgramsListingComponent implements OnInit {
  loading = true;
  rows: ProgramRow[] = [];
  page = 1;
  size = 100;
  total: number | null = null;

  ngOnInit() {
    this.load();
  }

  load() {
    this.loading = true;
    const url = `/api/programs/?page=${this.page}&size=${this.size}`;
    fetch(url)
      .then((r) => {
        if (!r.ok) console.error('GET', url, '->', r.status, r.statusText);
        return r.json();
      })
      .then((data: any) => {
        if (Array.isArray(data)) {
          this.rows = data as ProgramRow[];
          this.total = null;
        } else if (data && Array.isArray(data.items)) {
          this.rows = data.items as ProgramRow[];
          this.total = typeof data.total === 'number' ? data.total : null;
        } else {
          this.rows = [];
          this.total = null;
        }
      })
      .catch((err) => {
        console.error('Fetch programs failed:', url, err);
        this.rows = [];
        this.total = null;
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

  trackById(_: number, r: ProgramRow) {
    return r.id;
  }
}
