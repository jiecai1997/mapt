import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MappageComponent } from './mappage.component';

describe('MappageComponent', () => {
  let component: MappageComponent;
  let fixture: ComponentFixture<MappageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MappageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MappageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
