import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

type CohortStatus = 'Active' | 'Completed' | 'Upcoming' | 'Planning';

interface CohortRow {
  name: string;          // "Spring 2024"
  subgroups: string[];   // ["A1", "A2"] or []
  status: CohortStatus;  // pill
}

@Component({
  selector: 'app-cohorts-listing',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cohorts-listing.component.html',
  styleUrls: ['./cohorts-listing.component.scss']
})
export class CohortsListingComponent implements OnInit {
  loading = true;
  rows: CohortRow[] = [];

  ngOnInit() {
    // TODO: replace with real fetch
    // fetch('/api/cohorts').then(r => r.json()).then((data: CohortRow[]) => { this.rows = data; this.loading = false; });
    setTimeout(() => {
      this.rows = [
        { name: 'Spring 2024', subgroups: ['A1', 'A2', 'B1'], status: 'Active' },
        { name: 'Fall 2023',   subgroups: ['Evening'],        status: 'Completed' },
        { name: 'Summer 2024', subgroups: ['Designers'],      status: 'Upcoming' },
        { name: 'Winter 2024', subgroups: [],                 status: 'Planning' },
      ];
      this.loading = false;
    }, 400);
  }

  trackByName(_: number, r: CohortRow) { return r.name; }
}
