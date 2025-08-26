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
  styleUrls: ['./programs-listing.component.scss']
})
export class ProgramsListingComponent implements OnInit {
  loading = true;
  rows: ProgramRow[] = [];

  ngOnInit() {
    // TODO: replace with real fetch
    // fetch('/api/programs').then(r => r.json()).then((data: ProgramRow[]) => { this.rows = data; this.loading = false; });
    setTimeout(() => {
      this.rows = [
        { id: 1, name: 'Data Science Bootcamp', periods: 144 },
        { id: 2, name: 'Web Development',       periods: 108 },
        { id: 3, name: 'UX/UI Design',          periods: 72  },
        { id: 4, name: 'DevOps Engineering',    periods: 126 },
        { id: 5, name: 'Mobile Development',    periods: 90  },
      ];
      this.loading = false;
    }, 300);
  }

  trackById(_: number, r: ProgramRow) { return r.id; }
}
