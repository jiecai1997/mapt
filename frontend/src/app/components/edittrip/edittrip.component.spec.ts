import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EdittripComponent } from './edittrip.component';

describe('EdittripComponent', () => {
  let component: EdittripComponent;
  let fixture: ComponentFixture<EdittripComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EdittripComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EdittripComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
