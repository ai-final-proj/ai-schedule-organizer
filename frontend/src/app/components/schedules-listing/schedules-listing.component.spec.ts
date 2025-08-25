import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SchedulesListingComponent } from './schedules-listing.component';

describe('SchedulesListingComponent', () => {
  let component: SchedulesListingComponent;
  let fixture: ComponentFixture<SchedulesListingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SchedulesListingComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SchedulesListingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
