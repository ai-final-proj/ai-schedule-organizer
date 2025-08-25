import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CohortsListingComponent } from './cohorts-listing.component';

describe('CohortsListingComponent', () => {
  let component: CohortsListingComponent;
  let fixture: ComponentFixture<CohortsListingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CohortsListingComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CohortsListingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
