import { Component, EventEmitter, Input, Output, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';

export interface ScheduleDetailModel {
  id: number;
  name: string;
  description?: string | null;
  cohort?: string | null;
  subgroup?: string | null;
  program?: { id: number; name: string } | null;
}

export interface PeriodRow {
  id: number;
  name: string;
  description?: string | null;
  instructor?: string | null;
  category?: string | null;
}

@Component({
  selector: 'app-schedule-detail',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './schedule-detail.component.html',
  styleUrls: ['./schedule-detail.component.scss'],
})
export class ScheduleDetailComponent implements OnInit {
  @Input() schedule: ScheduleDetailModel | null = null;
  @Input() periods: PeriodRow[] | null = null;
  @Output() back = new EventEmitter<void>();

  activeTab: 'details' | 'periods' = 'details';
  id!: number;
  loading = false;
  error: string | null = null;

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit() {
    this.id = Number(this.route.snapshot.paramMap.get('id'));

    const qpTab = (this.route.snapshot.queryParamMap.get('tab') ?? 'details') as
      | 'details'
      | 'periods';
    this.activeTab = qpTab;

    const stateSchedule = history.state?.schedule;
    if (!this.schedule && stateSchedule && stateSchedule.id === this.id) {
      this.schedule = this.normalizeSchedule(stateSchedule);
    }

    void this.loadDetail();
  }

  goBack() {
    this.router.navigate(['/schedules']);
  }

  setTab(tab: 'details' | 'periods') {
    this.activeTab = tab;
  }

  private async loadDetail() {
    this.loading = true;
    this.error = null;

    try {
      const response = await fetch(`/api/schedules/${this.id}`);
      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = await response.json();
      if (data?.schedule) {
        this.schedule = this.normalizeSchedule(data.schedule);
      }
      this.periods = Array.isArray(data?.periods)
        ? data.periods.map((p: any) => this.normalizePeriod(p))
        : [];
    } catch (err) {
      console.error('Failed to load schedule detail', err);
      this.error = 'Unable to load schedule details.';
    } finally {
      this.loading = false;
    }
  }

  private normalizeSchedule(raw: any): ScheduleDetailModel {
    return {
      id: Number(raw?.id ?? this.id),
      name: raw?.name ?? 'Schedule',
      description: raw?.description ?? null,
      cohort: raw?.cohort ?? null,
      subgroup: raw?.subgroup ?? null,
      program: raw?.program
        ? {
            id: Number(raw.program.id),
            name: raw.program.name ?? 'Program',
          }
        : null,
    };
  }

  private normalizePeriod(raw: any): PeriodRow {
    return {
      id: Number(raw?.id ?? 0),
      name: raw?.name ?? 'Period',
      description: raw?.description ?? null,
      instructor: raw?.instructor ?? null,
      category: raw?.category ?? null,
    };
  }
}
