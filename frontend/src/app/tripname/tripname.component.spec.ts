import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TripnameComponent } from './tripname.component';

describe('TripnameComponent', () => {
  let component: TripnameComponent;
  let fixture: ComponentFixture<TripnameComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TripnameComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TripnameComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
