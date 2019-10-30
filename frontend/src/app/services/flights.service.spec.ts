import { TestBed } from '@angular/core/testing';

import { FlightsService } from './flights.service';

describe('FlightsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: FlightsService = TestBed.get(FlightsService);
    expect(service).toBeTruthy();
  });
});
