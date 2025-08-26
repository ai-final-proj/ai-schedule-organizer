import { Component } from '@angular/core';
import {NavigationEnd, Router, RouterLink, RouterOutlet} from '@angular/router';
import { SidebarComponent } from './components/sidebar/sidebar.component';
import {filter, Subscription} from 'rxjs';
import {NgIf} from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, SidebarComponent, RouterLink, NgIf],
  standalone: true,
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'AI Schedule Organizer';
  showFab = true;
  private sub: Subscription;
  sidebarCollapsed = false;

  constructor(private router: Router) {
    this.sub = this.router.events
      .pipe(filter((e): e is NavigationEnd => e instanceof NavigationEnd))
      .subscribe(e => {
        // hide on /chat or /chat/*
        const url = e.urlAfterRedirects || e.url;
        this.showFab = !/^\/chat(\/|$)/.test(url);
      });
  }

  toggleSidebar() {
    this.sidebarCollapsed = !this.sidebarCollapsed;
  }

  ngOnDestroy() { this.sub?.unsubscribe(); }
}
