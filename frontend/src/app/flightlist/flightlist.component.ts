import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-flightlist',
  templateUrl: './flightlist.component.html',
  styleUrls: ['./flightlist.component.css']
})
export class FlightlistComponent implements OnInit {
  tripname: string = "New Trip"
  flights = [];

  sampleAirports = ['RDU', 'Raleigh-Durham International Airport', 'SEA', 'ORD', 'BWI', 'IAD', 'Dulles International Airport'];

  constructor() {
    this.addFlight(); //start with one flight
    this.sampleAirports.sort(); //sort sample airports alphabetically
  }

  ngOnInit() {
  }

  getAirportSuggestions(query): any {
    if(query){
      query = query.toLowerCase(); //ignore case
      return this.sampleAirports.filter(airport => airport.toLowerCase().startsWith(query));
    }else{
      return this.sampleAirports;
    }
  }

  removeFlight(index): void{
    this.flights.splice(index, 1);
  }

  addFlight(): void{
    this.flights.push({
      obj: {
        dep: {},
        arr: {}
      },
      forms: {
        dep: {
          date: new FormControl(new Date())
        },
        arr: {
          date: new FormControl(new Date())
        }
      }
    });
  }

  submit(): void {
    console.log({
      tripname: 'mytrip',
      flights: this.flights.map(flight => flight.obj)
    });
  }
}
