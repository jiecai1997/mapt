import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddtripComponent } from './addtrip.component';

describe('AddtripComponent', () => {
  let component: AddtripComponent;
  let fixture: ComponentFixture<AddtripComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddtripComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddtripComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
