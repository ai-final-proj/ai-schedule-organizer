import { Routes } from '@angular/router';
import { UsersListingComponent } from './components/users-listing/users-listing.component';
import { CohortsListingComponent } from './components/cohorts-listing/cohorts-listing.component';
import { SchedulesListingComponent } from './components/schedules-listing/schedules-listing.component';
import { ScheduleDetailComponent } from './components/schedule-detail/schedule-detail.component';
import { ProgramsListingComponent } from './components/programs-listing/programs-listing.component';
import { ChatScreenComponent } from './components/chat-screen/chat-screen.component';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'users' },
  { path: 'users', component: UsersListingComponent },
  { path: 'cohorts', component: CohortsListingComponent },
  { path: 'schedules', component: SchedulesListingComponent },
  { path: 'schedules/:id', component: ScheduleDetailComponent },
  { path: 'programs', component: ProgramsListingComponent },
  { path: 'chat', component: ChatScreenComponent },
  { path: '**', redirectTo: 'users' },
];
