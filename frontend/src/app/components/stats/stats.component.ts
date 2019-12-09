import { Component, OnInit } from '@angular/core';
import { FlightsService } from '@app/services/flights.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.css']
})
export class StatsComponent implements OnInit {
  stats: Array<any> = [];

  constructor(private router: Router, private flightsService: FlightsService) { }

  ngOnInit() {
    this.flightsService.getStats().subscribe(result => {
      if(result['success'] == 'true'){
        this.stats = result['stats'];
      }else{
          this.router.navigate([''])
      }
    });
  }

}
