import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface UserRow {
  name: string;
  email: string;
  role?: string;
  role_id?: number;
  status?: string; // backend: 'active' | 'inactive'
  cohort?: string; // e.g., "Spring 2024" or "N/A"
  subgroup?: string; // e.g., "A1", "Evening", or "N/A"
}

@Component({
  selector: 'app-users-listing',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './users-listing.component.html',
  styleUrls: ['./users-listing.component.scss'],
})
export class UsersListingComponent implements OnInit {
  loading = true;
  rows: UserRow[] = [];

  // Pagination state
  page = 1;
  size = 20;
  total: number | null = null; // backend currently returns array only

  ngOnInit() {
    this.load();
  }

  load() {
    this.loading = true;
    const url = `/api/users/?page=${this.page}&size=${this.size}`;
    fetch(url)
      .then((r) => {
        if (!r.ok) console.error('GET', url, '->', r.status, r.statusText);
        return r.json();
      })
      .then((data: any) => {
        if (Array.isArray(data)) {
          this.rows = data as UserRow[];
          this.total = null;
        } else if (data && Array.isArray(data.items)) {
          this.rows = data.items as UserRow[];
          this.total = typeof data.total === 'number' ? data.total : null;
        } else {
          this.rows = [];
          this.total = null;
        }
      })
      .catch((err) => {
        console.error('Fetch users failed:', url, err);
        this.rows = [];
        this.total = null;
      })
      .finally(() => (this.loading = false));
  }

  // Computed pagination helpers
  get hasPrev() {
    return this.page > 1;
  }
  get hasNext() {
    if (this.total == null) return this.rows.length === this.size; // unknown total
    return this.page * this.size < this.total;
  }
  get totalPages(): number | null {
    if (this.total == null) return null;
    return Math.max(1, Math.ceil(this.total / this.size));
  }

  // UI event handlers
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

  trackByEmail(_: number, r: UserRow) {
    return r.email;
  }
}
