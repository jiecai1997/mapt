import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FlightlistComponent } from './flightlist.component';

describe('FlightlistComponent', () => {
  let component: FlightlistComponent;
  let fixture: ComponentFixture<FlightlistComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FlightlistComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FlightlistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
