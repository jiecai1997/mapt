import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-flightlist',
  templateUrl: './flightlist.component.html',
  styleUrls: ['./flightlist.component.css']
})
export class FlightlistComponent implements OnInit {
  sampleAirports = ['RDU', 'Raleigh-Durham International Airport', 'SEA', 'ORD', 'BWI', 'IAD', 'Dulles International Airport'];

  trip = {name: 'New Trip', flights: []}

  constructor() {
    this.addFlight(); //start with one flight
    this.sampleAirports.sort(); //sort sample airports alphabetically
  }

  ngOnInit() {
  }

  getAirportSuggestions(query: string): any {
    if(query){
      query = query.toLowerCase(); //ignore case
      return this.sampleAirports.filter(airport => airport.toLowerCase().startsWith(query));
    }else{
      return this.sampleAirports;
    }
  }

  removeFlight(index: number): void{
    this.trip.flights.splice(index, 1);
  }

  addFlight(): void{
    this.trip.flights.push({
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
    this.trip.flights = this.trip.flights.map(flight => flight.obj); // remove references to form controls
    console.log(this.trip);
  }
}
