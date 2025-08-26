import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

type UserStatus = 'Active' | 'Inactive';
type UserRole = 'Student' | 'Instructor' | 'Admin';

interface UserRow {
  name: string;
  email: string;
  role: UserRole;
  status: UserStatus;
  cohort: string;      // e.g., "Spring 2024" or "N/A"
  subgroup: string;    // e.g., "A1", "Evening", or "N/A"
}

@Component({
  selector: 'app-users-listing',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './users-listing.component.html',
  styleUrls: ['./users-listing.component.scss']
})
export class UsersListingComponent implements OnInit {
  loading = true;
  rows: UserRow[] = [];

  ngOnInit() {
    // TODO: replace with real fetch
    // Example:
    // this.loading = true;
    // fetch('/api/users')
    //   .then(r => r.json())
    //   .then((data: UserRow[]) => { this.rows = data; })
    //   .finally(() => this.loading = false);
    // fetch('/api/users').then(r => r.json()).then(data => { this.rows = data; this.loading = false; });
    setTimeout(() => {
      this.rows = [
        { name: 'Alice Johnson',  email: 'alice.johnson@example.com',  role: 'Student',    status: 'Active',   cohort: 'Spring 2024', subgroup: 'A1' },
        { name: 'Bob Smith',      email: 'bob.smith@example.com',      role: 'Instructor', status: 'Active',   cohort: 'N/A',         subgroup: 'N/A' },
        { name: 'Charlie Brown',  email: 'charlie.brown@example.com',  role: 'Student',    status: 'Inactive', cohort: 'Fall 2023',   subgroup: 'B2' },
        { name: 'Diana Ross',     email: 'diana.ross@example.com',     role: 'Admin',      status: 'Active',   cohort: 'N/A',         subgroup: 'N/A' },
        { name: 'Ethan Hunt',     email: 'ethan.hunt@example.com',     role: 'Student',    status: 'Active',   cohort: 'Spring 2024', subgroup: 'A2' },
      ];
      this.loading = false;
    }, 400);
  }

  trackByEmail(_: number, r: UserRow) { return r.email; }
}
