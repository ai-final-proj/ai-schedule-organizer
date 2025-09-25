import { Component, Input } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { NgFor, NgSwitch, NgSwitchCase } from '@angular/common';

type SidebarItem = {
  title: string;
  link: string;
  key: 'users' | 'cohorts' | 'schedules' | 'programs' | 'chat';
};

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, NgFor, NgSwitch, NgSwitchCase],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss'],
})
export class SidebarComponent {
  @Input() collapsed = false;
  // You can add/remove routes here; icons are mapped in the template via ngSwitch
  items: SidebarItem[] = [
    { title: 'Users', link: '/users', key: 'users' },
    { title: 'Cohorts', link: '/cohorts', key: 'cohorts' },
    { title: 'Schedules', link: '/schedules', key: 'schedules' },
    { title: 'Programs', link: '/programs', key: 'programs' },
    // optional:
    // { title: 'Chat',      link: '/chat',      key: 'chat' },
  ];
}
