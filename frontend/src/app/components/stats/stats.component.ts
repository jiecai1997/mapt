import { Component, OnInit } from '@angular/core';
import { FlightsService } from '@app/services/flights.service';

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.css']
})
export class StatsComponent implements OnInit {
  stats: Array<any> = [];

  constructor(private flightsService: FlightsService) { }

  ngOnInit() {
    this.flightsService.getStats().subscribe(result => {
      this.stats = result['stats'];
    });
  }

}
